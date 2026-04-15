from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def append_session_row(data_dir: Path, payload: dict[str, Any]) -> Path:
    ensure_directory(data_dir)
    target = data_dir / "participants.csv"
    fieldnames = [
        "timestamp_utc",
        "event",
        "prolific_pid",
        "study_id",
        "session_id",
        "consent_given",
        "response_count",
    ]

    row = {key: payload.get(key, "") for key in fieldnames}
    file_exists = target.exists()
    with target.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
    return target


def append_response_event(data_dir: Path, payload: dict[str, Any]) -> Path:
    ensure_directory(data_dir)
    target = data_dir / "response_events.jsonl"
    event = {
        "timestamp_utc": utc_now_iso(),
        **payload,
    }
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event) + "\n")
    return target
