FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt /var/lib/dpkg /var/lib/cache /var/lib/log

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY docs/docs_requirements.txt /tmp/docs_requirements.txt
RUN pip install -r /tmp/docs_requirements.txt

WORKDIR /tmp/

# copy everything in root dir to image. customize here and/or in .dockerignore
COPY . /tmp/

# Install your package in editable mode
RUN pip install -e .