FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y install xinetd && rm -rf /var/lib/apt/lists/*

RUN adduser ctf

COPY challenge /home/ctf/challenge
COPY flag /home/ctf/flag
COPY flag /flag

RUN chown -R root:ctf /home/ctf
RUN chmod -R 550 /home/ctf

COPY ctf /etc/xinetd.d/ctf
RUN chown root:root /etc/xinetd.d/ctf
RUN chmod 400 /etc/xinetd.d/ctf

COPY run_xinetd.sh /etc/run_xinetd.sh
RUN chown root:root /etc/run_xinetd.sh
RUN chmod 500 /etc/run_xinetd.sh

COPY run_challenge.sh /home/ctf/run_challenge.sh
RUN chown root:ctf /home/ctf/run_challenge.sh
RUN chmod 450 /home/ctf/run_challenge.sh

RUN dd if=/dev/urandom bs=16 count=1 > /home/ctf/aes_ecb_key.txt

CMD /etc/run_xinetd.sh

EXPOSE 31337
