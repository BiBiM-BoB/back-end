FROM golang:1.19.1 AS builder

WORKDIR /go/src/app

RUN git clone https://github.com/zricethezav/gitleaks.git && \
    cd gitleaks && \
    make build 

FROM debian:buster

COPY --from=builder /go/src/app/gitleaks/gitleaks /bin/gitleaks

WORKDIR /src

ENTRYPOINT [ "gitleaks" ]