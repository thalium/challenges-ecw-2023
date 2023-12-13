FROM ubuntu:20.04
RUN apt-get update
RUN apt-get upgrade -y
RUN useradd -d /home/yogosha/ -m -p yogosha -s /bin/bash yogosha

RUN echo "yogosha:yogosha" | chpasswd

WORKDIR /home/yogosha

COPY ynetd .
COPY task .
COPY flag.txt .
RUN chown -R root:root /home/yogosha/

USER yogosha
EXPOSE 1234

CMD ./ynetd -p 1234 ./task

