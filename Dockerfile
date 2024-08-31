FROM python:3.12-slim

WORKDIR /transaction

ENV POETRY_VERSION=1.8.3

RUN apt-get update && apt-get -y upgrade && pip install "poetry==${POETRY_VERSION}"
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY ./src/app ./app

EXPOSE 8002

COPY ./alembic.ini  .
COPY ./src/migration ./src/migration

ENTRYPOINT [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002" ]
