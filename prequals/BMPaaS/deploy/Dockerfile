FROM ubuntu:latest
RUN apt-get update && apt-get -y install python3 socat
COPY BMPaaS.py .
COPY flag.bmp .
EXPOSE 31337
CMD socat TCP-LISTEN:31337,reuseaddr,fork EXEC:"python3 BMPaaS.py"
