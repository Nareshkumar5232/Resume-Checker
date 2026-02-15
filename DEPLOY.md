Deployment options

1) Deploy to Render (recommended quick option)
- Create a new Web Service in Render and connect your GitHub repo.
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Render will detect the `Dockerfile` or just use the build/start commands above.

2) Deploy with Docker (any host)
- Build locally:

```bash
docker build -t ats-resume-checker:latest .
```

- Run locally:

```bash
docker run -p 5000:5000 ats-resume-checker:latest
```

3) Deploy to Railway / Fly / other hosts
- Use `requirements.txt` and set the start command to `gunicorn app:app`.

Notes:
- The spaCy model `en_core_web_sm` is included in `requirements.txt` so it will be installed during build.
- NLTK stopwords are downloaded at runtime by `ATSFreindly.py` (the script calls `nltk.download('stopwords')`).
- If you see issues with spaCy models, run `python -m spacy download en_core_web_sm` on the host or include `en-core-web-sm` in requirements (already present).

If you want, I can:
- Create a Git repo and push these changes for you,
- Deploy directly to Render (I can prepare a step-by-step or create a render.yaml), or
- Add CI workflow (GitHub Actions) to build and deploy automatically.
