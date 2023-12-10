FROM debian:bookworm-slim as root

RUN apt-get update \
    && DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends libpython3.11-minimal python3 python3-dev python3-requests python3-xmltodict \
    && rm -rf /var/lib/apt/lists* 

WORKDIR /root
COPY callquery.py /root/
COPY qrz_query.py /root/
COPY settings.cfg /root/






