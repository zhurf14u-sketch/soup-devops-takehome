# Pin the official multi-platform manifest. Renovate proposes deliberate digest updates.
FROM python:3.12-slim@sha256:aa943ce411423c7582288f18707ff66eddcbaeb510502d747a72aeb34f30d159

WORKDIR /app
COPY src/ /app/src/
COPY pyproject.toml /app/
RUN useradd --create-home --uid 10001 appuser \
    && python -m compileall -q /app/src \
    && chown -R appuser:appuser /app
USER 10001
ENV PYTHONPATH=/app/src
ENTRYPOINT ["python", "-m", "soup_cli.cli"]
