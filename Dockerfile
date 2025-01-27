FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ENV PATH="/root/.local/bin:$PATH"

RUN apt-get update && \
    apt-get install -y gcc default-libmysqlclient-dev build-essential pkg-config && \
    apt-get clean

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /app/

RUN pip install -U pip setuptools wheel
RUN pip install --upgrade pip

RUN pip install mysqlclient

RUN poetry install --no-root

COPY . /app/

RUN poetry run python wallet/manage.py migrate
CMD ["poetry", "run", "python", "wallet/manage.py", "runserver", "0.0.0.0:8000"]
