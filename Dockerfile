FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN addgroup --system fincodeguard \
    && adduser --system --ingroup fincodeguard fincodeguard

COPY pyproject.toml README.md ./
COPY src ./src

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -e ".[dev]"

COPY tests ./tests
COPY benchmark ./benchmark

COPY .coveragerc ./
COPY scripts ./scripts

COPY RELEASE_CHECKLIST.md ./
COPY docs ./docs

COPY prompts ./prompts
COPY candidates ./candidates

RUN chown -R fincodeguard:fincodeguard /app

USER fincodeguard

CMD ["pytest"]