from experiment.logic.storage import append_response_event, append_session_row, utc_now_iso
from experiment.surveys.demo import CHOICE_ITEM, RATING_ITEM, STUDY_TITLE
from flask import Blueprint, current_app, redirect, render_template, request, session, url_for

bp = Blueprint("main", __name__)


def capture_prolific_params() -> None:
    for query_key, session_key in (
        ("PROLIFIC_PID", "prolific_pid"),
        ("STUDY_ID", "study_id"),
        ("SESSION_ID", "session_id"),
    ):
        value = request.args.get(query_key)
        if value:
            session[session_key] = value


def session_payload() -> dict[str, str]:
    return {
        "prolific_pid": session.get("prolific_pid", ""),
        "study_id": session.get("study_id", ""),
        "session_id": session.get("session_id", ""),
    }


@bp.route("/")
def index():
    capture_prolific_params()
    return render_template(
        "index.html",
        participant=session_payload(),
        study_title=STUDY_TITLE,
    )


@bp.route("/consent", methods=["GET", "POST"])
def consent():
    if request.method == "POST":
        capture_prolific_params()
        session["consent_given"] = request.form.get("consent") == "yes"
        if session["consent_given"]:
            return redirect(url_for("main.survey"))
        return redirect(url_for("main.index"))
    return render_template(
        "consent.html",
        participant=session_payload(),
        study_title=STUDY_TITLE,
    )


@bp.route("/survey", methods=["GET", "POST"])
def survey():
    if not session.get("consent_given"):
        return redirect(url_for("main.consent"))

    if request.method == "POST":
        responses = {
            CHOICE_ITEM["name"]: request.form.get(CHOICE_ITEM["name"], ""),
            RATING_ITEM["name"]: request.form.get(RATING_ITEM["name"], ""),
        }
        session["responses"] = responses
        append_response_event(
            current_app.config["RAW_DATA_DIR"],
            {
                "event": "survey_submit",
                **session_payload(),
                "consent_given": bool(session.get("consent_given")),
                "responses": responses,
            },
        )
        return redirect(url_for("main.complete"))

    return render_template(
        "survey.html",
        participant=session_payload(),
        study_title=STUDY_TITLE,
        choice_item=CHOICE_ITEM,
        rating_item=RATING_ITEM,
    )


@bp.route("/complete")
def complete():
    if not session.get("consent_given"):
        return redirect(url_for("main.consent"))

    if not session.get("completion_logged"):
        metadata = {
            "timestamp_utc": utc_now_iso(),
            "event": "study_complete",
            **session_payload(),
            "consent_given": bool(session.get("consent_given")),
            "response_count": len(session.get("responses", {})),
        }
        append_session_row(current_app.config["RAW_DATA_DIR"], metadata)
        session["completion_logged"] = True

    completion_code = current_app.config["COMPLETION_CODE"]
    prolific_return_url = current_app.config["PROLIFIC_RETURN_URL"]
    if prolific_return_url:
        complete_url = prolific_return_url
    else:
        complete_url = url_for("main.index", _external=True)
    return render_template(
        "complete.html",
        completion_code=completion_code,
        complete_url=complete_url,
        participant=session_payload(),
        prolific_return_url=prolific_return_url,
        study_title=STUDY_TITLE,
    )
