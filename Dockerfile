FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    vim\
    nano\
    wget\
    curl\
    python3.9\
    pip

RUN mkdir -p /home/user
WORKDIR /home/user

COPY ./docker/reqs.txt /tmp/reqs.txt
RUN python3 -m pip install --upgrade pip
RUN pip install -r /tmp/dockerdir/reqs.txt
