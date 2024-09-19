FROM python:slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt /var/lib/dpkg /var/lib/cache /var/lib/log

COPY docs/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /tmp/


# copy everything in root dir to image. customize here and/or in .dockerignore
COPY . /tmp/