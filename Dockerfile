FROM python:3.10.11-slim-buster as builder

RUN pip install poetry==1.4.2 && \
    poetry config experimental.new-installer false

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /tmp

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

FROM python:3.10.11-slim-buster as base

ENV VIRTUAL_ENV=/tmp/.venv \
    PATH="/tmp/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /opt/app
ADD . /opt/app

FROM builder as builder-test

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

FROM base as test

COPY --from=builder-test ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /opt/app
