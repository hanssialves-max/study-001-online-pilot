# Psych Lab Template

Reusable Flask template for online psychological surveys and simple experiments.

## What this template standardizes

- a participant flow of landing -> consent -> survey -> completion
- standard Prolific parameter capture
- flat-file study data storage for early lab use
- a clear split between app plumbing and study-specific logic
- a copy-and-rename workflow for new studies
- a documented default deployment path for Render

This v1 is intentionally aimed at surveys and simple experiments, not high-precision timing tasks.

## Folder structure

```text
psych-lab-template/
  app/
    __init__.py
    routes.py
    templates/
    static/
  experiment/
    config.py
    logic/
    surveys/
    stimuli/
  data/
    raw/
    exports/
  docs/
    consent.md
    procedure.md
    prolific.md
    deployment.md
    launch-checklist.md
  tests/
  .vscode/
  render.yaml
  requirements.txt
  run.py
```

## Quick start

1. Open this folder in VS Code.
2. Create a virtual environment:
   `python -m venv .venv`
3. Install dependencies:
   `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`
4. Start the local pilot app:
   `.\.venv\Scripts\python.exe run.py`
5. Open:
   `http://127.0.0.1:5000`

To test a Prolific-style launch locally, use a URL like:

`http://127.0.0.1:5000/?PROLIFIC_PID=test_pid&STUDY_ID=test_study&SESSION_ID=test_session`

## How the lab should use this template

1. Copy the entire `psych-lab-template` folder.
2. Rename the copy to the new study name.
3. Create a fresh `.venv` inside the copied folder.
4. Update the files in `docs/` first.
5. Replace the demo survey items in `experiment/surveys/`.
6. Implement study logic in `experiment/logic/`.
7. Adapt participant routing in `app/routes.py` only if the standard flow is not enough.
8. Pilot locally before any deployment.

## Prolific defaults

The template captures and carries these standard query parameters:

- `PROLIFIC_PID`
- `STUDY_ID`
- `SESSION_ID`

The completion page supports:

- a replaceable completion code via `COMPLETION_CODE`
- an optional Prolific return URL via `PROLIFIC_RETURN_URL`

## Flat-file data storage

This v1 writes local pilot data into `data/raw`:

- `participants.csv` for participant/session completion rows
- `response_events.jsonl` for submitted response events

This is suitable for early lab pilots and small studies. It is not the right long-term choice for high-concurrency production deployment.

## VS Code working layout

Recommended layout for lab members:

- left: Explorer
- center: code and docs
- right: Codex panel
- bottom: Terminal

Useful files to pin while building a study:

- `README.md`
- `docs/prolific.md`
- `docs/launch-checklist.md`
- `app/routes.py`
- one active file under `experiment/`

## Render deployment

This template includes a starter `render.yaml` and a deployment guide in `docs/deployment.md`.

Recommended environment variables on Render:

- `SECRET_KEY`
- `COMPLETION_CODE`
- `PROLIFIC_RETURN_URL`

## What to change first in a real study

- replace the demo consent text
- replace the demo survey items
- set a real completion code or return URL
- decide what response data should be stored
- review the launch checklist before recruiting participants
