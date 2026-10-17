FROM python:3.11-slim

# poppler for pdftotext (quote verifiers); Node for the Claude Code CLI the Agent SDK drives
RUN apt-get update && apt-get install -y --no-install-recommends \
        poppler-utils nodejs npm ca-certificates git curl \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g @anthropic-ai/claude-code && npm cache clean --force

# One venv serves the harness and the project's scripts (.venv/bin/python is linked to it)
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" PYTHONUNBUFFERED=1
COPY harness/requirements.txt /app/harness/requirements.txt
RUN pip install --no-cache-dir -r /app/harness/requirements.txt

# The project as built in Part A is the seed workspace (data, .claude, scripts, signed-off outputs)
COPY . /app/project
COPY harness /app/harness

# Claude Code refuses to bypass permissions as root: run as an unprivileged user
RUN useradd -m -u 1000 agent && mkdir -p /data && chown -R agent:agent /data /app
USER agent
ENV HOME=/home/agent DATA_ROOT=/data SEED_DIR=/app/project VENV_DIR=/opt/venv
WORKDIR /app/harness
EXPOSE 8080
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080}"]
