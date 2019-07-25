FROM python:3.7

MAINTAINER "Dharwin Perez <dharwin@urbvan.com>"

# Copy requirements files
COPY ./src/pyproject.toml /tmp/pyproject.toml
COPY ./src/poetry.lock /tmp/poetry.lock

# Install dependencies
WORKDIR /tmp
RUN pip install -U poetry
RUN poetry config settings.virtualenvs.create false && poetry install --no-interaction

# Copy code project
WORKDIR /app
COPY ./src/manage.py /app/manage.py
COPY ./src/core /app/core
COPY ./src/apps /app/apps
COPY ./src/config /app/config

# Expose ports
EXPOSE 9000
