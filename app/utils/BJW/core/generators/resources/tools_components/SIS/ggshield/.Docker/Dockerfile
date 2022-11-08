FROM ubuntu:22.04

RUN sed -re 's/([a-z]{2}.)?archive.ubuntu.com/mirror.kakao.com/g' -e 's/security.ubuntu.com/mirror.kakao.com/g' -i.bak /etc/apt/sources.list
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends python3-pip git && \
    pip install -U ggshield && \
    apt-get clean && \
    apt-get autoclean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/cache/* && \
    rm -rf /var/lib/log/*

WORKDIR /src  
    
ENTRYPOINT [ "ggshield" ]