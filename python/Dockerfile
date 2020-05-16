FROM python:3.8-slim AS builder

WORKDIR /app

RUN set -x \
  && apt-get -y update \
  && apt-get -y upgrade \
  && apt-get install --no-install-recommends -yq \
  curl \
  gcc \
  python-dev \
  && apt-get clean \
  && apt-get autoclean \
  && apt-get autoremove \
  && rm -rf /tmp/* /var/tmp/* \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 \
  && export PATH=/root/.poetry/bin:$PATH \
  && poetry self update \
  && poetry config virtualenvs.in-project true \
  && poetry install --no-dev


FROM python:3.8-slim

WORKDIR /app
COPY --from=builder /app/.venv /.venv
COPY . .

EXPOSE 50051
ENV PYTHONPATH PYTHONPATH:/app
ENTRYPOINT [ "/.venv/bin/python3" ]
CMD ["src/commands/server.py"]