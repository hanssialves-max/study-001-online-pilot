# Prolific Integration Notes

## Standard parameters

Common Prolific URL parameters:

- `PROLIFIC_PID`
- `STUDY_ID`
- `SESSION_ID`

## For each study, confirm

- recruitment settings
- eligibility filters
- estimated duration
- payment rate
- completion code or redirect
- handling of screen-outs and returns

## Default template behavior

- captures parameters from the launch URL
- stores them in the Flask session for downstream pages
- shows them during the local pilot flow
- records completion metadata in `data/raw/participants.csv`
- records submitted demo responses in `data/raw/response_events.jsonl`

## Recommended routine

1. Document the Prolific study URL used for launch.
2. Confirm parameter capture locally before launch.
3. Test completion handling with a pilot run.
4. Keep the exact completion logic version archived with the study.

## Pilot checklist

1. Launch the local app with example Prolific parameters in the URL.
2. Confirm those values appear on the landing page and study page.
3. Confirm participants cannot skip straight to the study without consent.
4. Submit a pilot response and confirm new files appear in `data/raw`.
5. Confirm the completion page shows the intended code or return URL.
6. Retest the full flow after any routing or survey changes.
