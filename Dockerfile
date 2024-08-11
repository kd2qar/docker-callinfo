#FROM debian:bookworm-slim as root
FROM debian:stable-slim

MAINTAINER Mark Vincett <kd2qar@gmail.com>

RUN apt-get update  \
     && apt-get -y upgrade  \
     && DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends python3-requests python3-xmltodict python3-certifi python3-urllib3 ca-certificates \
     && rm -rf /var/lib/apt/lists*
WORKDIR /root
COPY callquery.py /root/
COPY sql/temptable.sql /root/
COPY callbooks/ /root/callbooks/
COPY settings.cfg /root/
RUN chmod +x /root/callquery.py
