FROM debian:12
MAINTAINER Rune Juhl Jacobsen <rune.juhl@atea.dk>

RUN adduser local

RUN apt-get update && \
    apt-get install -y ansible git python3-pytest python3-pytest-forked python3-pip
