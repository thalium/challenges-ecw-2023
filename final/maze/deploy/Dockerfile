FROM debian:latest
ENV DEBIAN_FRONTEND=noninteractive TERM=xterm-color

RUN apt update -y && \
    apt upgrade -y
	

RUN apt install -y supervisor apache2 python3 pip git


RUN pip install requests
RUN pip install names 

RUN /etc/init.d/apache2 start && \
    rm /var/www/html/index.html

#IMPORTANT : 
COPY ./src/main.sh /root/
COPY ./src/Knuth_quotes  /root/
COPY ./src/script.py /root/
COPY ./src/flag /root/
COPY ./src/html/000-default.conf /root/000-default.conf 
COPY ./src/html/fancy-index-main/ /var/www/html/fancy-index/


# supervisor
COPY ./src/supervisor/ /etc/supervisor/conf.d/
RUN chmod 700 /etc/supervisor && chmod 700 /var/log/supervisor && chmod +x /root/main.sh
	

RUN apt-get clean && \
	rm -rf /var/lib/apt/lists/* /var/tmp/* /tmp/* && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

RUN sed -i -e 's/\^M//g' /root/main.sh && \
	sed -i -e 's/\r$//' /root/main.sh && \
    sed -i -e 's/\^M//g' /root/flag && \
	sed -i -e 's/\r$//' /root/flag

	
CMD ["/usr/bin/supervisord","-c","/etc/supervisor/supervisord.conf"]