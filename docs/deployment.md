# Deployment Notes

Before deployment:

- replace the development secret key
- disable debug mode
- decide where data will be stored
- verify consent and debrief text
- test the full Prolific flow
- test on desktop and mobile

## Default host

Render is the default recommended host for this template because it keeps setup simple for the lab while staying close to a normal Python deployment model.

## Render steps

1. Push the study folder to a Git repository.
2. Create a new Render web service from that repository.
3. Set the root directory to the study folder if the repo contains multiple projects.
4. Use `pip install -r requirements.txt` as the build command.
5. Use `gunicorn run:app` as the start command.
6. Set environment variables:
   - `SECRET_KEY`
   - `COMPLETION_CODE`
   - `PROLIFIC_RETURN_URL`
7. Deploy and run a full pilot using a Prolific-style URL.

## Portability

The app is kept intentionally deployment-neutral. If you move away from Render later, the main things to carry over are:

- Python dependency installation
- the `gunicorn run:app` entrypoint
- the environment variables above
- writable storage expectations for `data/raw`

Possible hosting options:

- Render
- Railway
- PythonAnywhere
- university-managed server
