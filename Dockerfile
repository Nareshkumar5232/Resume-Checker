FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:${PORT:-5000}", "--workers", "3", "app:app"]
