FROM python:3.11-slim-bookworm

RUN apt-get update \
  && apt-get -y install --no-install-recommends git ssh \
  && rm -fr /var/lib/apt/lists/*

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY process-manager-no-kafka.json /
