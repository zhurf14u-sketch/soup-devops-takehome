# Pin the official multi-platform manifest. Renovate proposes deliberate digest updates.
FROM python:3.15-slim@sha256:65a65fc7b30b06cb6df4930fd4650697cb23f4c2698ab81fc87e4b031bc36928

WORKDIR /app
COPY src/ /app/src/
COPY pyproject.toml /app/
RUN useradd --create-home --uid 10001 appuser \
    && python -m compileall -q /app/src \
    && chown -R appuser:appuser /app
USER 10001
ENV PYTHONPATH=/app/src
ENTRYPOINT ["python", "-m", "soup_cli.cli"]
