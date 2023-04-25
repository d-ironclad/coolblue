FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /coolblue

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Project requirements
RUN pip install pipenv
COPY Pipfile Pipfile.lock /coolblue/
RUN pipenv install --system

COPY ./coolblue /coolblue/

CMD ['gunicorn' 'solver_api.wsgi' '--bind' '0.0.0.0:8000' '--workers' '4' '--threads' '4']