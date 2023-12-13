FROM php:apache
WORKDIR /var/www/html
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y
RUN apt full-upgrade -y
RUN apt install cron -y
RUN mkdir uploads

COPY parser /var/www/html/
COPY index.php /var/www/html/
COPY flag /flag
COPY clean.sh /root/clean.sh

RUN chown www-data:www-data ./uploads
RUN chown root:root /var/www/html
RUN chmod 755 /var/www/html
RUN chmod 744 /root/clean.sh
RUN chmod 744 /flag
RUN chmod 755 /var/www/html/parser
RUN crontab -l | { cat; echo "* * * * * bash /root/clean.sh"; } | crontab -

CMD (cron -f &) && apache2ctl -D FOREGROUND

EXPOSE 80
