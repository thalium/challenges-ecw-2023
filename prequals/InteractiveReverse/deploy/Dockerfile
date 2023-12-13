FROM ubuntu:latest

RUN apt-get update && apt-get -y install python3 socat

COPY serverside_vm.py .

EXPOSE 42080
CMD socat TCP-LISTEN:42080,reuseaddr,fork EXEC:"python3 -u serverside_vm.py"
