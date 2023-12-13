FROM ubuntu:jammy-20230816 AS challenge
SHELL ["/bin/bash", "-c"]

RUN apt-get update -qq \
 && apt-get install -qq \
    libassuan0 \
    libfakeroot \
    libglib2.0-dev \
    libksba8 \
    libldap-2.5-0 \
    libnpth0 \
    libpython3-dev \
    libtool \
    locales \
 && rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8

ENV LANG="en_US.UTF-8"
ENV LANGUAGE="en_US:en"
ENV LC_ALL="en_US.UTF-8"
ENV LC_CTYPE="C.UTF-8"

RUN mkdir /app
WORKDIR /app

COPY build/qemu-riscv64-shadow .
COPY build/sysroot sysroot
COPY build/calculator-shadow .
COPY flag.txt .

RUN printf '%s\n' \
    '#!/usr/bin/env bash' \
    'LANG="en_US.UTF-8"' \
    'LANGUAGE="en_US:en"' \
    'LC_ALL="en_US.UTF-8"' \
    'LC_CTYPE="C.UTF-8"' \
    '/app/qemu-riscv64-shadow -L /app/sysroot /app/calculator-shadow' \
 > run
RUN chmod +x run

FROM pwn.red/jail
COPY --from=challenge / /srv

ENV JAIL_TIME=0
ENV JAIL_PIDS=0
ENV JAIL_MEM=0
