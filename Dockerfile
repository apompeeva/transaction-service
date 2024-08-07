FROM python:3.12-slim

WORKDIR /transaction

ENV POETRY_VERSION=1.8.3

RUN apt-get update && apt_get upgrade pip && pip install "poetry==${POETRY_VERSION}"
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY ./src/app ./app

EXPOSE 8002

ENTRYPOINT [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002" ]
