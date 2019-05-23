FROM buildpack-deps:16.04-curl

RUN apt-get update \
    && apt-get install -y --no-install-recommends bzip2 \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
