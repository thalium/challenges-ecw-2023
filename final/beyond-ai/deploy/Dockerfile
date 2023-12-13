FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive TERM=xterm-color

RUN apt update -y && \
    apt install cron supervisor python3-pip apache2 mariadb-server php php-mysqli -y && \
    python3 -m pip install playwright && \
    playwright install chromium --with-deps && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

COPY ./src/apache2/apache2.conf /etc/apache2/
COPY ./src/supervisor/supervisord.conf /etc/supervisor/conf.d/
COPY ./src/root/ /root/

WORKDIR /root

RUN tar zxvf wp.tgz -C /var/www/html && \
    rm /var/www/html/index.html && \
    service mariadb start && \
    mysql < wp-init.sql && \
    rm /root/wp.* && \
    chmod +x /root/database-interact.sh && \
    echo '*/2 * * * * root python3 /root/bot.py' >> /etc/crontab && \
    echo 'FLAG{80607c59bc156ab3c6c300950c668373}\nN3v3r_TRuSt_aN_AI_t0_bu!ld_y0ur_@ppl!c@t!ons' > /flag.txt

EXPOSE 80

CMD ["/usr/bin/supervisord","-c","/etc/supervisor/supervisord.conf"]
