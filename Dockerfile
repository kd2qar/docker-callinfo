FROM debian:bookworm-slim as root
#FROM debian:stable-slim

LABEL MAINTAINER="Mark Vincett <kd2qar@gmail.com>"

RUN apt-get update  \
     && apt-get -y upgrade  \
     && DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends python3-requests python3-xmltodict python3-certifi python3-urllib3  python3-mysqldb python3-pymysql  ca-certificates \
     && rm -rf /var/lib/apt/lists/*

ADD dot.bashrc /root/.bashrc
COPY <<EOF /root/.vimrc
set background=dark
syntax on
set mouse=
set shiftwidth=2
set tabstop=4
EOF

WORKDIR /callinfo
ADD --chmod=755 callquery.py /callinfo/
ADD sql/temptable.sql /callinfo/
ADD callbooks/ /callinfo/callbooks/
ADD settings.cfg /callinfo/
#COPY clublog_check.py /clublog/
#RUN chmod +x /callinfo/callquery.py
#RUN chmod +x /clublog/clublog_check.py

