FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    REFLEX_TELEMETRY_ENABLED=false \
    COOKIE_SECURE=true

RUN apt-get update && apt-get install -y --no-install-recommends curl unzip ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd --create-home --uid 10001 app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN chown app:app /app
USER app
COPY --chown=app:app rxconfig.py ./
COPY --chown=app:app reflex.lock ./reflex.lock
COPY --chown=app:app Codeboxd_main ./Codeboxd_main
COPY --chown=app:app assets ./assets
RUN python -m reflex init

EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=180s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:3000/ping', timeout=4)"
CMD ["python", "-m", "reflex", "run", "--env", "prod", "--single-port", "--frontend-port", "3000", "--backend-port", "3000", "--backend-host", "0.0.0.0"]
