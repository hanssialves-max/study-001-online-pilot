import csv
import json
import shutil
from pathlib import Path
from uuid import uuid4

from app import create_app


def make_local_tmp_dir() -> Path:
    target = Path(__file__).resolve().parent / "_tmp" / uuid4().hex
    target.mkdir(parents=True, exist_ok=True)
    return target


def test_app_creation():
    app = create_app()
    assert app is not None


def test_core_routes_and_prolific_capture():
    tmp_path = make_local_tmp_dir()
    try:
        app = create_app()
        app.config["TESTING"] = True
        app.config["RAW_DATA_DIR"] = tmp_path
        client = app.test_client()

        response = client.get(
            "/?PROLIFIC_PID=p1&STUDY_ID=s1&SESSION_ID=ss1"
        )
        assert response.status_code == 200
        assert b"p1" in response.data

        consent_get = client.get("/consent")
        assert consent_get.status_code == 200

        survey_without_consent = client.get("/survey", follow_redirects=False)
        assert survey_without_consent.status_code == 302

        consent_post = client.post("/consent", data={"consent": "yes"}, follow_redirects=False)
        assert consent_post.status_code == 302
        assert consent_post.headers["Location"].endswith("/survey")

        survey_get = client.get("/survey")
        assert survey_get.status_code == 200
        assert b"Who is more EC?" in survey_get.data
    finally:
        shutil.rmtree(tmp_path, ignore_errors=True)


def test_completion_writes_flat_files():
    tmp_path = make_local_tmp_dir()
    try:
        app = create_app()
        app.config["TESTING"] = True
        app.config["RAW_DATA_DIR"] = tmp_path
        client = app.test_client()

        client.get("/?PROLIFIC_PID=p2&STUDY_ID=s2&SESSION_ID=ss2")
        client.post("/consent", data={"consent": "yes"})
        completion = client.post(
            "/survey",
            data={
                "more_ec": "Hans Alves",
                "study_quality": "7",
            },
            follow_redirects=True,
        )

        assert completion.status_code == 200
        assert b"Thank you for taking part" in completion.data

        csv_file = tmp_path / "participants.csv"
        jsonl_file = tmp_path / "response_events.jsonl"
        assert csv_file.exists()
        assert jsonl_file.exists()

        with csv_file.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        assert len(rows) == 1
        assert rows[0]["prolific_pid"] == "p2"
        assert rows[0]["response_count"] == "2"

        with jsonl_file.open("r", encoding="utf-8") as handle:
            event = json.loads(handle.readline())
        assert event["prolific_pid"] == "p2"
        assert event["responses"]["study_quality"] == "7"
    finally:
        shutil.rmtree(tmp_path, ignore_errors=True)
