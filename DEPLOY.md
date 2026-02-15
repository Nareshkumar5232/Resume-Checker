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

4) Deploy to Vercel (notes and steps)
- Add `vercel.json` to the project root (provided) to tell Vercel to treat `app.py` as a Python entrypoint.
- Recommended Vercel Project settings / build command:
	- Build Command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
	- Output Directory: leave blank or set to `.`

Notes and caveats for Vercel:
- Vercel runs Python code as serverless functions; large language models and heavy runtime downloads (spaCy, NLTK data) may increase cold-start times or fail due to size/time limits.
- If `python -m spacy download en_core_web_sm` fails during build, consider pre-packaging the model or deploying to a VM/container host (Render, Railway, Docker) instead.
- To deploy:
	1. Push your repo to GitHub.
	2. In Vercel, choose "Import Project" → select the GitHub repo.
	3. In Build & Output settings set the Build Command above and leave Output Directory empty.
	4. Deploy and monitor build logs. If the build fails on model installation, switch to Render or Docker.

If you want, I can also:
- Add a GitHub Action that runs tests and optionally triggers a Vercel redeploy,
- Prepare a lightweight serverless-friendly version (no spaCy model download) that uses a smaller NLP approach for Vercel.
