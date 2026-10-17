"""Hosted harness for the Procurement Audit Planning Agent.

A FastAPI app that owns a workspace copy of the project (data, .claude skills and
agents, scripts, outputs), runs each pipeline stage with the Claude Agent SDK,
and puts the two human gates (risk approval, pack sign-off) in the browser.
"""
from __future__ import annotations

import asyncio
import datetime
import json
import os
import re
import secrets
import shutil
import subprocess
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse

import runner

SEED = Path(os.environ.get("SEED_DIR", "/app/project"))
DATA_ROOT = Path(os.environ.get("DATA_ROOT", "/data"))
WS = DATA_ROOT / "workspace"
RUNS_DIR = DATA_ROOT / "runs"
SPEND_FILE = DATA_ROOT / "spend.json"
VENV = Path(os.environ.get("VENV_DIR", "/opt/venv"))
PASSCODE = os.environ.get("RUN_PASSCODE", "")
MAX_TOTAL_USD = float(os.environ.get("MAX_TOTAL_USD", "150"))
STATIC = Path(__file__).parent / "static"

app = FastAPI(title="Procurement Audit Planner")
RUNS: dict[str, runner.Run] = {}
ACTIVE: dict[str, asyncio.Task] = {}
LOCK = asyncio.Lock()

STAGE_INFO = {
    "extract-rules": "1 · Extract rules (skill)",
    "analysts": "2 · Spend + findings analysts (sub-agents)",
    "spend-analyst": "2a · Spend analyst only",
    "findings-analyst": "2b · Findings analyst only",
    "risk-assessor": "3 · Risk assessor (sub-agent)",
    "revise-register": "4 · Revise register from auditor decisions",
    "team": "5 · Agent team: planner, challenger, qa-reviewer",
}


# ------------------------------------------------------------------ workspace

def copy_seed(dst: Path):
    ignore = shutil.ignore_patterns(".venv", ".git", "__pycache__", ".DS_Store", "harness", "Dockerfile", "fly.toml")
    shutil.copytree(SEED, dst, ignore=ignore, dirs_exist_ok=True)


def link_venv():
    v = WS / ".venv"
    if v.is_symlink() or v.exists():
        return
    v.symlink_to(VENV, target_is_directory=True)


# Built code that ships with each deploy; outputs, agent memory and the
# spend-analyst's own scripts are left as the runs made them.
SYNCED = [".claude/agents", ".claude/skills", ".claude/settings.json", "CLAUDE.md",
          "data", "scripts/checks", "scripts/verify_history.py"]


def sync_code():
    ignore = shutil.ignore_patterns("__pycache__", ".DS_Store")
    for rel in SYNCED:
        src, dst = SEED / rel, WS / rel
        if src.is_dir():
            shutil.copytree(src, dst, ignore=ignore, dirs_exist_ok=True)
        elif src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def init_workspace():
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    if not (WS / ".seeded").exists():
        WS.mkdir(parents=True, exist_ok=True)
        copy_seed(WS)
        (WS / ".seeded").write_text(datetime.datetime.now().isoformat())
    else:
        sync_code()
    link_venv()
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    for f in sorted(RUNS_DIR.glob("*.json")):
        try:
            d = json.loads(f.read_text())
            r = runner.Run(id=d["id"], stage=d["stage"], started=d["started"])
            r.finished, r.status, r.summary = d.get("finished"), d["status"], d.get("summary", "")
            r.cost_usd, r.events = d.get("cost_usd", 0), d.get("events", [])
            if r.status == "running":
                r.status, r.finished = "failed", r.finished or r.started
                r.summary = "interrupted by a server restart"
            RUNS[r.id] = r
        except Exception:  # noqa: BLE001
            pass


@app.on_event("startup")
async def startup():
    init_workspace()


def py(*args, timeout=300) -> tuple[int, str]:
    p = subprocess.run([str(WS / ".venv" / "bin" / "python"), *args], cwd=WS,
                       capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout + p.stderr).strip()


def spent() -> float:
    try:
        return json.loads(SPEND_FILE.read_text())["usd"]
    except Exception:  # noqa: BLE001
        return 0.0


def add_spend(usd: float):
    SPEND_FILE.write_text(json.dumps({"usd": spent() + usd}))


def need_passcode(code: str | None):
    if not PASSCODE:
        raise HTTPException(503, "RUN_PASSCODE is not configured on the server")
    if not code or not secrets.compare_digest(code, PASSCODE):
        raise HTTPException(401, "wrong passcode")


def busy():
    return any(not t.done() for t in ACTIVE.values())


# ------------------------------------------------------------------- status

def register_revision() -> int | None:
    p = WS / "outputs" / "risk-register.md"
    if not p.exists():
        return None
    m = re.search(r"\*\*Revision (\d+)\*\*", p.read_text(encoding="utf-8"))
    return int(m.group(1)) if m else 0


def review_state() -> dict:
    p = WS / "outputs" / "review.md"
    if not p.exists():
        return {"exists": False}
    t = p.read_text(encoding="utf-8")
    verdict = re.search(r"## Verdict\s*\n+(.+)", t)
    sig = {k: (re.search(rf"^{re.escape(k)}[^:\n]*:[ \t]*(.*)$", t, re.M) or [None, ""])[1].strip()
           for k in ("Signed off by", "Date", "Decision", "Comment")}
    return {"exists": True, "verdict": verdict.group(1).strip() if verdict else "",
            "signoff": sig, "mtime": p.stat().st_mtime}


def challenge_counts() -> dict:
    p = WS / "outputs" / "challenges.md"
    if not p.exists():
        return {}
    counts: dict[str, int] = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 8 and re.fullmatch(r"\d+", cells[0]):
            s = cells[-1].strip("* ").lower() or "open"
            counts[s] = counts.get(s, 0) + 1
    return counts


@app.get("/api/status")
async def status():
    o = WS / "outputs"
    gate_rc, gate_out = (None, "")
    if (o / "risk-register.json").exists():
        gate_rc, gate_out = await asyncio.to_thread(py, ".claude/skills/audit-program/build_pack.py", "--gate")
    exists = lambda *ps: all((o / p).exists() for p in ps)  # noqa: E731
    active = next((rid for rid, t in ACTIVE.items() if not t.done()), None)
    return {
        "api_key": bool(os.environ.get("ANTHROPIC_API_KEY")),
        "passcode_required": True,
        "model": runner.MODEL,
        "spent_usd": round(spent(), 2), "max_total_usd": MAX_TOTAL_USD,
        "active_run": active,
        "stages": {
            "extract-rules": exists("rules.json"),
            "analysts": exists("analytics.json", "history.json"),
            "risk-assessor": exists("risk-register.md", "auditor-comments.md"),
            "gate": gate_rc == 0,
            "team": exists("planning-memo.md", "risk-control-matrix.md", "audit-program.md", "review.md"),
        },
        "register_revision": register_revision(),
        "gate_output": gate_out,
        "challenges": challenge_counts(),
        "review": review_state(),
        "stage_labels": STAGE_INFO,
    }


# --------------------------------------------------------------------- runs

@app.post("/api/run/{stage}")
async def start_run(stage: str, x_passcode: str | None = Header(default=None)):
    need_passcode(x_passcode)
    if stage not in runner.STAGES:
        raise HTTPException(404, "unknown stage")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise HTTPException(503, "ANTHROPIC_API_KEY is not configured on the server")
    if spent() >= MAX_TOTAL_USD:
        raise HTTPException(429, f"spend cap of ${MAX_TOTAL_USD:.0f} reached")
    async with LOCK:
        if busy():
            raise HTTPException(409, "another run is in progress")
        if stage == "team":
            rc, out = await asyncio.to_thread(py, ".claude/skills/audit-program/build_pack.py", "--gate")
            if rc != 0:
                raise HTTPException(409, "gate not closed: " + out[-600:])
        run = runner.Run(id=time.strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:4], stage=stage)
        if stage == "team":
            run.log("lead", "text", "gate check passed:\n" + out)
        RUNS[run.id] = run

        async def go():
            try:
                await runner.execute(run, WS, RUNS_DIR)
            except asyncio.CancelledError:
                run.status, run.finished = "stopped", time.time()
                run.log("harness", "text", "run stopped by the user")
                runner.save_run(run, RUNS_DIR)
            finally:
                add_spend(run.cost_usd)

        ACTIVE[run.id] = asyncio.create_task(go())
    return {"id": run.id}


@app.post("/api/stop")
async def stop_run(x_passcode: str | None = Header(default=None)):
    need_passcode(x_passcode)
    for rid, t in ACTIVE.items():
        if not t.done():
            RUNS[rid].stop_requested = True
            t.cancel()
            return {"stopped": rid}
    return {"stopped": None}


@app.get("/api/runs")
async def list_runs():
    rs = sorted(RUNS.values(), key=lambda r: r.started, reverse=True)
    return [{k: v for k, v in r.to_dict().items() if k != "events"} for r in rs[:50]]


@app.get("/api/runs/{rid}")
async def get_run(rid: str, since: int = 0):
    if rid not in RUNS:
        raise HTTPException(404)
    return RUNS[rid].to_dict(since)


# -------------------------------------------------------------------- files

VIEWABLE = {".md", ".json", ".csv", ".txt", ".py"}


def safe(path: str) -> Path:
    p = (WS / path).resolve()
    if not str(p).startswith(str(WS.resolve()) + os.sep):
        raise HTTPException(400, "bad path")
    return p


@app.get("/api/files")
async def files():
    out = []
    for top in ("outputs", "data", ".claude/skills", ".claude/agents", "scripts", "CLAUDE.md"):
        base = WS / top
        items = [base] if base.is_file() else sorted(base.rglob("*")) if base.exists() else []
        for f in items:
            if f.is_file() and "__pycache__" not in f.parts and f.name != ".DS_Store":
                out.append({"path": str(f.relative_to(WS)), "size": f.stat().st_size,
                            "mtime": f.stat().st_mtime, "viewable": f.suffix in VIEWABLE})
    return out


@app.get("/api/file")
async def file(path: str, raw: bool = False):
    p = safe(path)
    if not p.is_file():
        raise HTTPException(404)
    if raw or p.suffix not in VIEWABLE:
        return FileResponse(p, filename=p.name)
    text = p.read_text(encoding="utf-8", errors="replace")
    truncated = len(text) > 400_000
    if p.suffix == ".csv":
        lines = text.splitlines()
        truncated, text = len(lines) > 201, "\n".join(lines[:201])
    return {"path": path, "suffix": p.suffix, "text": text[:400_000], "truncated": truncated}


# ------------------------------------------------------------- human gates

ROW_RE = re.compile(r"^\|\s*(R-\d{2,})\s*\|")


@app.get("/api/gate")
async def gate():
    p = WS / "outputs" / "auditor-comments.md"
    if not p.exists():
        raise HTTPException(404, "run the risk assessor first")
    rows, reviewer = [], ""
    text = p.read_text(encoding="utf-8")
    for line in text.splitlines():
        if ROW_RE.match(line):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            rows.append({"risk": c[0], "title": c[1], "score": c[2], "band": c[3],
                         "decision": c[4], "comment": c[5] if len(c) > 5 else ""})
        m = re.match(r"^Reviewer:\s*(.*)$", line)
        if m:
            reviewer = m.group(1).strip()
    return {"revision": register_revision(), "reviewer": reviewer, "rows": rows}


@app.post("/api/gate")
async def save_gate(request: Request, x_passcode: str | None = Header(default=None)):
    need_passcode(x_passcode)
    if busy():
        raise HTTPException(409, "a run is in progress")
    body = await request.json()
    reviewer = str(body.get("reviewer", "")).strip()
    decisions = {r["risk"]: r for r in body.get("rows", [])}
    if not reviewer:
        raise HTTPException(400, "reviewer name is required")
    for rid, r in decisions.items():
        d = r.get("decision", "")
        if d not in {"Approve", "Amend", "Reject", ""}:
            raise HTTPException(400, f"{rid}: decision must be Approve, Amend or Reject")
        if d in {"Amend", "Reject"} and not str(r.get("comment", "")).strip():
            raise HTTPException(400, f"{rid}: {d} needs a comment")
    p = WS / "outputs" / "auditor-comments.md"
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if m and m.group(1) in decisions:
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            while len(c) < 6:
                c.append("")
            r = decisions[m.group(1)]
            c[4] = r.get("decision", "")
            c[5] = str(r.get("comment", "")).replace("|", "/").replace("\n", " ").strip()
            line = "| " + " | ".join(c) + " |"
        elif line.startswith("Reviewer:"):
            line = f"Reviewer: {reviewer}  "
        elif line.startswith("Date:"):
            line = f"Date: {datetime.date.today().isoformat()}"
        out.append(line)
    # The builder's template has no reviewer lines: add them under the Register line.
    if not any(l.startswith("Reviewer:") for l in out):
        at = next((i + 1 for i, l in enumerate(out) if l.startswith("Register:")), 1)
        out[at:at] = ["", f"Reviewer: {reviewer}  ", f"Date: {datetime.date.today().isoformat()}"]
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    return {"saved": len(decisions)}


@app.post("/api/signoff")
async def signoff(request: Request, x_passcode: str | None = Header(default=None)):
    need_passcode(x_passcode)
    body = await request.json()
    name = str(body.get("name", "")).strip()
    decision = body.get("decision")
    comment = str(body.get("comment", "")).replace("\n", " ").strip()
    if not name or decision not in {"sign off", "return to the team"}:
        raise HTTPException(400, "name and a decision (sign off / return to the team) are required")
    st = review_state()
    if not st.get("exists"):
        raise HTTPException(409, "no review.md yet: run the agent team first")
    if decision == "sign off" and "READY FOR SIGN-OFF" not in st["verdict"]:
        raise HTTPException(409, f"verdict is '{st['verdict']}': sign-off is blocked")
    p = WS / "outputs" / "review.md"
    t = p.read_text(encoding="utf-8")
    vals = {"Signed off by": name, "Date": datetime.date.today().isoformat(),
            "Decision": decision, "Comment": comment}
    for k, v in vals.items():
        t = re.sub(rf"^({re.escape(k)}[^:\n]*:)[ \t]*.*$", lambda m, v=v: f"{m.group(1)} {v}", t, count=1, flags=re.M)
    p.write_text(t, encoding="utf-8")
    return review_state()


# ------------------------------------------------------------ checks/reset

@app.post("/api/checks")
async def checks():
    if busy():
        raise HTTPException(409, "a run is in progress")
    rc, out = await asyncio.to_thread(py, "scripts/checks/run_checks.py")
    return {"exit": rc, "output": out[-6000:]}


@app.post("/api/reset")
async def reset(request: Request, x_passcode: str | None = Header(default=None)):
    need_passcode(x_passcode)
    if busy():
        raise HTTPException(409, "a run is in progress")
    mode = (await request.json()).get("mode")
    if mode not in {"saved", "fresh"}:
        raise HTTPException(400, "mode must be saved or fresh")
    shutil.rmtree(WS / "outputs", ignore_errors=True)
    if mode == "saved":
        shutil.copytree(SEED / "outputs", WS / "outputs")
    else:
        (WS / "outputs").mkdir()
    for d in ("scripts",):
        if mode == "saved":
            shutil.copytree(SEED / d, WS / d, dirs_exist_ok=True)
    return {"reset": mode}


@app.post("/api/passcode")
async def check_passcode(x_passcode: str | None = Header(default=None)):
    need_passcode(x_passcode)
    return {"ok": True}


@app.get("/healthz")
async def healthz():
    return {"ok": True}


@app.get("/")
async def index():
    return FileResponse(STATIC / "index.html")


@app.exception_handler(HTTPException)
async def http_error(_, exc: HTTPException):
    return JSONResponse({"error": exc.detail}, status_code=exc.status_code)
