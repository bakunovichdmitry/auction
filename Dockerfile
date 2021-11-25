FROM python:3.9.7

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.1.10

RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# Project initialization:
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /app

ENTRYPOINT ginicorn auction.wsgi --bind 0.0.0.0:8000