FROM ubuntu:20.04

RUN apt -y update
RUN apt -y install libssl-dev ncat

RUN adduser ctf

COPY ./files /home/ctf/server

RUN chown -R root:ctf /home/ctf
RUN chmod -R 550 /home/ctf

WORKDIR /home/ctf/server

EXPOSE 1337

CMD ["su", "-", "ctf", "-c", "cd /home/ctf/server && /home/ctf/server/launch.sh"]