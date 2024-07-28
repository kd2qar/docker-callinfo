FROM debian:bookworm-slim as root
#FROM python:slim

#RUN apt-get update \
#    && DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends libpython3.11-minimal python3 python3-dev python3-requests python3-xmltodict ca-certificates \
#    && rm -rf /var/lib/apt/lists* 
RUN apt-get update  \
     && apt-get -y upgrade  \
     && DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends python3-requests python3-xmltodict python3-certifi python3-urllib3 ca-certificates \
     && rm -rf /var/lib/apt/lists*
WORKDIR /root
COPY callquery.py /root/
COPY qrz_query.py /root/
COPY hamqth_query.py /root/
COPY settings.cfg /root/

