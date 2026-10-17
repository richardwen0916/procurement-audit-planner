"""Agent runner for the hosted harness.

Loads the project's own skills and agents from .claude/ and runs them with the
Claude Agent SDK inside the workspace. Stages 1-3 run one agent session each;
stage 5 runs the planner / challenger / qa-reviewer team, which coordinates
through a send_message tool this module implements (the harness is the lead).
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    create_sdk_mcp_server,
    tool,
)

MODEL = os.environ.get("MODEL", "claude-opus-5-5")
SESSION_BUDGET_USD = float(os.environ.get("SESSION_BUDGET_USD", "15"))
TEAM_TIMEOUT_S = int(os.environ.get("TEAM_TIMEOUT_S", str(90 * 60)))
TEAM_MAX_TURNS_PER_MEMBER = int(os.environ.get("TEAM_MAX_TURNS_PER_MEMBER", "14"))
TEAM = ["planner", "challenger", "qa-reviewer"]
LEAD_ALIASES = {"lead", "main", "team-lead", "the lead"}


# --------------------------------------------------------------------------- runs

@dataclass
class Run:
    id: str
    stage: str
    started: float = field(default_factory=time.time)
    finished: float | None = None
    status: str = "running"          # running | ok | failed | stopped
    summary: str = ""
    cost_usd: float = 0.0
    events: list = field(default_factory=list)
    stop_requested: bool = False

    def log(self, agent: str, kind: str, text: str):
        self.events.append({"t": round(time.time() - self.started, 1), "agent": agent,
                            "kind": kind, "text": text[:4000]})

    def to_dict(self, since: int = 0):
        return {"id": self.id, "stage": self.stage, "started": self.started,
                "finished": self.finished, "status": self.status, "summary": self.summary,
                "cost_usd": round(self.cost_usd, 4), "n_events": len(self.events),
                "events": self.events[since:]}


def save_run(run: Run, runs_dir: Path):
    runs_dir.mkdir(parents=True, exist_ok=True)
    (runs_dir / f"{run.id}.json").write_text(json.dumps(run.to_dict()), encoding="utf-8")


# ------------------------------------------------------------------ definitions

def read_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2)


def agent_definition(ws: Path, name: str) -> tuple[list[str], str]:
    meta, body = read_frontmatter(ws / ".claude" / "agents" / f"{name}.md")
    tools = [t.strip() for t in meta.get("tools", "Bash, Read, Write, Edit, Glob, Grep").split(",") if t.strip()]
    if meta.get("memory"):
        body += (f"\n\n## Memory location\nYour persistent memory directory is "
                 f"`.claude/agent-memory/{name}/` (index `MEMORY.md`). Read it at the start; "
                 f"save how-to lessons only, as your instructions above say.")
    return tools, body


def skill_body(ws: Path, name: str) -> str:
    return read_frontmatter(ws / ".claude" / "skills" / name / "SKILL.md")[1]


HOSTED_NOTE = """

## Hosted harness
You are running inside the hosted Procurement Audit Planner harness, not an
interactive terminal. There is no human to answer questions mid-run: if an input
is missing or malformed, stop and report it in your final message. The project
root is the current directory and `.venv/bin/python` is available. Keep your
final message short: what you produced, the verifier result, anything blocked.
"""


def options_for(ws: Path, tools: list[str], append: str, extra_tools=(), mcp=None) -> ClaudeAgentOptions:
    allowed = list(dict.fromkeys(tools + ["Skill"] + list(extra_tools)))
    return ClaudeAgentOptions(
        cwd=str(ws),
        model=MODEL,
        tools=[t for t in allowed if not t.startswith("mcp__")],
        allowed_tools=allowed,
        permission_mode="bypassPermissions",
        setting_sources=["project"],
        system_prompt={"type": "preset", "preset": "claude_code", "append": append + HOSTED_NOTE},
        mcp_servers=mcp or {},
        max_budget_usd=SESSION_BUDGET_USD,
        env={"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "0"},
    )


# --------------------------------------------------------------- message pump

def describe_tool(block: ToolUseBlock) -> str:
    i = block.input or {}
    if block.name == "Bash":
        return f"$ {i.get('command', '')}"
    for key in ("file_path", "path", "pattern", "skill"):
        if key in i:
            return f"{block.name} {i[key]}"
    if block.name.endswith("send_message"):
        return f"→ {i.get('to')}: {str(i.get('message', ''))[:200]}"
    return f"{block.name} {json.dumps(i)[:200]}"


async def drain(client: ClaudeSDKClient, run: Run, agent: str) -> str:
    """Consume one response; log text and tool calls; return the final result text.

    ResultMessage.total_cost_usd is cumulative for the session, so only the
    increase since the previous turn is added to the run's cost.
    """
    final = ""
    async for msg in client.receive_response():
        if isinstance(msg, AssistantMessage):
            for b in msg.content:
                if isinstance(b, TextBlock) and b.text.strip():
                    run.log(agent, "text", b.text.strip())
                elif isinstance(b, ToolUseBlock) and not b.name.endswith("send_message"):
                    run.log(agent, "tool", describe_tool(b))
        elif isinstance(msg, ResultMessage):
            total = msg.total_cost_usd or 0.0
            prev = getattr(client, "_cost_so_far", 0.0)
            run.cost_usd += max(total - prev, 0.0)
            client._cost_so_far = total
            final = msg.result or ""
            run.log(agent, "result", f"turn finished: {msg.num_turns} steps, "
                                     f"session cost ${total:.2f}"
                                     + (" (ERROR)" if msg.is_error else ""))
            if msg.is_error:
                raise RuntimeError(f"{agent}: {msg.subtype} {msg.errors or msg.result or ''}")
    return final


async def single_session(run: Run, ws: Path, agent: str, tools: list[str], append: str, prompt: str) -> str:
    run.log(agent, "start", prompt)
    async with ClaudeSDKClient(options=options_for(ws, tools, append)) as client:
        await client.query(prompt)
        result = await drain(client, run, agent)
    run.log(agent, "done", result or "(no final message)")
    return result


# ------------------------------------------------------------------- stages

async def stage_extract_rules(run: Run, ws: Path):
    await single_session(
        run, ws, "extract-rules", ["Bash", "Read", "Write", "Edit", "Glob", "Grep"],
        "## Skill: extract-rules\n" + skill_body(ws, "extract-rules"),
        "Run the extract-rules skill: convert data/contract-rules.pdf into outputs/rules.json "
        "and run the skill's verifier until it reports ALL CHECKS PASSED. Report rule and "
        "excluded counts.")


ANALYST_PROMPTS = {
    "spend-analyst": "Run the spend-analyst: produce outputs/analytics.json and "
                     "outputs/analytics-full/ and run your self-check.",
    "findings-analyst": "Run the findings-analyst: produce outputs/history.json and run "
                        "`.venv/bin/python scripts/verify_history.py outputs/history.json data/committee` "
                        "until it reports ALL CHECKS PASSED (it also checks the scoring_method layout).",
}


async def run_agent(run: Run, ws: Path, name: str):
    tools, body = agent_definition(ws, name)
    return await single_session(run, ws, name, tools, body, ANALYST_PROMPTS[name])


async def stage_analysts(run: Run, ws: Path):
    await asyncio.gather(run_agent(run, ws, "spend-analyst"), run_agent(run, ws, "findings-analyst"))


async def stage_risk_assessor(run: Run, ws: Path, revise: bool):
    tools, body = agent_definition(ws, "risk-assessor")
    prompt = ("Revise the register: apply the auditor's decisions recorded in "
              "outputs/auditor-comments.md and build the next revision."
              if revise else
              "Run the risk-assessor: build outputs/risk-register.md and the auditor "
              "decision template outputs/auditor-comments.md for the approval gate.")
    await single_session(run, ws, "risk-assessor", tools, body, prompt)


# ---------------------------------------------------------------- the team

class Team:
    """The harness acts as lead: it spawns three sessions and routes their messages."""

    def __init__(self, run: Run, ws: Path):
        self.run, self.ws = run, ws
        self.inbox = {n: asyncio.Queue() for n in TEAM}
        self.busy = {n: True for n in TEAM}
        self.turns = {n: 0 for n in TEAM}
        self.done: dict[str, str] = {}
        self.forwarded_to_qa = False
        self.stop = asyncio.Event()

    def _norm(self, to: str) -> str | None:
        t = to.strip().lower().lstrip("@")
        if t in LEAD_ALIASES:
            return "lead"
        for n in TEAM:
            if t == n or t.startswith(n) or (n == "qa-reviewer" and t in {"qa", "qa reviewer", "qa_reviewer"}):
                return n
        return None

    def make_tool(self, sender: str):
        team = self

        @tool("send_message",
              "Send a message to a teammate (planner, challenger, qa-reviewer) or to the lead "
              "(to: 'lead'). This is the team's SendMessage: your plain text output is not "
              "seen by anyone else. Messages to you arrive automatically at your next turn.",
              {"to": str, "message": str})
        async def send_message(args):
            target = team._norm(str(args.get("to", "")))
            text = str(args.get("message", "")).strip()
            if not target or not text:
                return {"content": [{"type": "text", "text":
                        "error: 'to' must be planner, challenger, qa-reviewer or lead, and 'message' non-empty"}],
                        "is_error": True}
            team.run.log(sender, "message", f"→ {target}: {text}")
            if target == "lead":
                team.on_lead_message(sender, text)
            else:
                await team.inbox[target].put(f"[message from {sender}]\n{text}")
            return {"content": [{"type": "text", "text": f"delivered to {target}"}]}

        return send_message

    def on_lead_message(self, sender: str, text: str):
        head = text.upper()
        for n, token in (("planner", "PLANNER DONE"), ("challenger", "CHALLENGER DONE"), ("qa-reviewer", "QA DONE")):
            if sender == n and token in head:
                self.done[n] = text
        if "BLOCKED" in head and sender == "planner":
            self.done["planner"] = text
            self.run.log("lead", "text", "Planner reported BLOCKED; stopping the team.")
            self.stop.set()
        # The qa-reviewer writes the final review only after the other two are done;
        # they report to the lead, so the lead tells it once (as in the local run).
        if {"planner", "challenger"} <= self.done.keys() and not self.forwarded_to_qa:
            self.forwarded_to_qa = True
            note = ("[message from lead]\nBoth done signals have reached the lead:\n"
                    f"- {self.done['planner'][:600]}\n- {self.done['challenger'][:600]}\n"
                    "Run the checks on the final version, write outputs/review.md and send QA DONE to the lead.")
            self.inbox["qa-reviewer"].put_nowait(note)
            self.run.log("lead", "message", "→ qa-reviewer: planner and challenger are done; write the final review.")
        if len(self.done) == len(TEAM):
            self.stop.set()

    async def member(self, name: str, first_prompt: str):
        tools, body = agent_definition(self.ws, name)
        server = create_sdk_mcp_server(name="team", version="1.0.0", tools=[self.make_tool(name)])
        opts = options_for(self.ws, tools, body, extra_tools=["mcp__team__send_message"], mcp={"team": server})
        self.run.log(name, "start", "spawned as teammate")
        async with ClaudeSDKClient(options=opts) as client:
            prompt = first_prompt
            while not self.stop.is_set():
                self.busy[name] = True
                self.turns[name] += 1
                await client.query(prompt)
                await drain(client, self.run, name)
                self.busy[name] = False
                if self.turns[name] >= TEAM_MAX_TURNS_PER_MEMBER:
                    self.run.log(name, "text", "turn limit reached")
                    return
                # wait for mail (or the stop signal)
                getter = asyncio.create_task(self.inbox[name].get())
                stopper = asyncio.create_task(self.stop.wait())
                await asyncio.wait({getter, stopper}, return_when=asyncio.FIRST_COMPLETED)
                if not getter.done():
                    getter.cancel()
                    return
                stopper.cancel()
                msgs = [getter.result()]
                while not self.inbox[name].empty():
                    msgs.append(self.inbox[name].get_nowait())
                prompt = "\n\n".join(msgs)

    async def supervise(self, started: float):
        nudged = False
        idle_since = None
        while not self.stop.is_set():
            await asyncio.sleep(5)
            if self.run.stop_requested or time.time() - started > TEAM_TIMEOUT_S:
                self.run.log("lead", "text", "stopping the team (stop requested or time limit)")
                self.stop.set()
                return
            quiet = not any(self.busy.values()) and all(q.empty() for q in self.inbox.values())
            if not quiet:
                idle_since = None
                continue
            idle_since = idle_since or time.time()
            if time.time() - idle_since < 20:
                continue
            if not nudged:
                nudged, idle_since = True, None
                for n in TEAM:
                    if n not in self.done:
                        self.inbox[n].put_nowait(
                            "[message from lead]\nThe team is idle and nothing is pending. If your part "
                            "is finished, send your DONE message to the lead now; otherwise carry on.")
                self.run.log("lead", "text", "team idle: asked unfinished teammates for their DONE status")
            else:
                self.run.log("lead", "text", "team idle after a nudge; stopping")
                self.stop.set()

    async def go(self):
        common = ("Phase 3 is starting and the auditor gate is CLOSED (the lead ran "
                  "build_pack.py --gate). Your teammates are {others}. Coordinate with them "
                  "directly using the mcp__team__send_message tool; the lead does not relay. ")
        prompts = {
            "planner": common.format(others="challenger and qa-reviewer") +
                "Start now: follow your instructions and the audit-program skill, build the pack, "
                "and announce PACK READY v1 to both teammates. When finished send PLANNER DONE to the lead.",
            "challenger": common.format(others="planner and qa-reviewer") +
                "Wait for the planner's PACK READY v1 before reviewing the pack (you may read the "
                "register, analytics.json and history.json now, then end your turn to wait). "
                "Write outputs/challenges.md, at most two rounds. When finished send CHALLENGER DONE "
                "to the lead with counts by status and the points for the auditor.",
            "qa-reviewer": common.format(others="planner and challenger") +
                "Wait for the planner's PACK READY message before checking (end your turn to wait). "
                "On each version run scripts/checks/run_checks.py and message failures to the planner. "
                "After the lead tells you the planner and challenger are done, write outputs/review.md "
                "and send QA DONE to the lead with the verdict.",
        }
        started = time.time()
        sup = asyncio.create_task(self.supervise(started))
        try:
            results = await asyncio.gather(*(self.member(n, prompts[n]) for n in TEAM), return_exceptions=True)
        finally:
            self.stop.set()
            sup.cancel()
        errors = [f"{n}: {r}" for n, r in zip(TEAM, results) if isinstance(r, Exception)]
        return errors


async def stage_team(run: Run, ws: Path):
    team = Team(run, ws)
    errors = await team.go()
    for e in errors:
        run.log("lead", "error", e)
    missing = [n for n in TEAM if n not in team.done]
    if errors or missing:
        raise RuntimeError("team did not finish: " + "; ".join(errors + [f"no DONE from {m}" for m in missing]))
    run.summary = team.done.get("qa-reviewer", "")[:400]


STAGES = {
    "extract-rules": stage_extract_rules,
    "analysts": stage_analysts,
    "spend-analyst": lambda run, ws: run_agent(run, ws, "spend-analyst"),
    "findings-analyst": lambda run, ws: run_agent(run, ws, "findings-analyst"),
    "risk-assessor": lambda run, ws: stage_risk_assessor(run, ws, revise=False),
    "revise-register": lambda run, ws: stage_risk_assessor(run, ws, revise=True),
    "team": stage_team,
}


import subprocess  # noqa: E402

PY = ".venv/bin/python"
# What each stage must leave behind; a run whose agent stopped and reported a
# problem (rather than producing these) is marked failed, not ok.
POSTCHECKS = {
    "extract-rules": [[PY, ".claude/skills/extract-rules/verify_quotes.py", "outputs/rules.json", "data/contract-rules.pdf"]],
    "spend-analyst": [[PY, "scripts/selfcheck.py"]],
    "findings-analyst": [[PY, "scripts/verify_history.py", "outputs/history.json", "data/committee"]],
    "analysts": [[PY, "scripts/selfcheck.py"],
                 [PY, "scripts/verify_history.py", "outputs/history.json", "data/committee"]],
    "risk-assessor": [["test", "-s", "outputs/risk-register.md"], ["test", "-s", "outputs/auditor-comments.md"]],
    "revise-register": [["test", "-s", "outputs/risk-register.md"]],
    "team": [[PY, "scripts/checks/run_checks.py"]],
}


def postcheck(run: Run, ws: Path) -> list[str]:
    failed = []
    for cmd in POSTCHECKS.get(run.stage, []):
        p = subprocess.run(cmd, cwd=ws, capture_output=True, text=True, timeout=600)
        tail = (p.stdout + p.stderr).strip().splitlines()[-3:]
        run.log("harness", "check" if p.returncode == 0 else "error",
                f"{' '.join(cmd[1:3] if cmd[0] == PY else cmd)} → exit {p.returncode}\n" + "\n".join(tail))
        if p.returncode != 0:
            failed.append(" ".join(cmd[1:2] if cmd[0] == PY else cmd))
    return failed


async def execute(run: Run, ws: Path, runs_dir: Path):
    try:
        await STAGES[run.stage](run, ws)
        failed = await asyncio.to_thread(postcheck, run, ws)
        if failed:
            raise RuntimeError("stage outputs failed their checks: " + ", ".join(failed))
        run.status = "stopped" if run.stop_requested else "ok"
    except Exception as e:  # noqa: BLE001
        run.status = "failed"
        run.log("harness", "error", f"{type(e).__name__}: {e}\n{traceback.format_exc()[-1500:]}")
        run.summary = run.summary or str(e)[:400]
    finally:
        run.finished = time.time()
        save_run(run, runs_dir)
