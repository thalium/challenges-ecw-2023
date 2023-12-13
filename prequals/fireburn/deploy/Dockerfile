FROM debian:bullseye-slim

LABEL maintainer="jacob.alberty@foundigital.com"

ENV PREFIX=/usr/local/firebird
ENV VOLUME=/firebird
ENV DEBIAN_FRONTEND noninteractive
ENV FBURL=https://github.com/FirebirdSQL/firebird/releases/download/v3.0.10/Firebird-3.0.10.33601-0.tar.bz2
ENV DBPATH=/firebird/data

# misc
RUN apt update -y && \
    apt upgrade -y

# supervisord
RUN apt install -y supervisor
COPY ./src/supervisor/ /etc/supervisor/conf.d/
RUN chmod 700 /etc/supervisor && chmod 700 /var/log/supervisor

# apache
RUN apt install -y apache2 libapache2-mod-php libfbclient2 wget && \
    wget https://github.com/FirebirdSQL/php-firebird/releases/download/v3.0.1/php_7.4.33-interbase-3.0.1-linux-x64.so && \
    mv php_7.4.33-interbase-3.0.1-linux-x64.so /usr/lib/php/20190902/ && \
    echo "" >> /etc/php/7.4/apache2/php.ini && \
    echo "[firebird]" >> /etc/php/7.4/apache2/php.ini && \
    echo "extension = php_7.4.33-interbase-3.0.1-linux-x64.so" >> /etc/php/7.4/apache2/php.ini && \
    rm -fr /var/www/html/* && \
    a2enmod rewrite
COPY ./src/apache/000-default.conf /etc/apache2/sites-available/000-default.conf
COPY ./src/html/ /var/www/html/

# firebird
RUN apt-get install -qy --no-install-recommends libicu67 libncurses6 libtommath1 netbase procps bzip2 ca-certificates \
    curl file g++ gcc libicu-dev libncurses-dev libtommath-dev make zlib1g-dev firebird3.0-utils
COPY ./src/firebird/build.sh ./build.sh
RUN chmod +x ./build.sh && \
    sync && \
    ./build.sh && \
    rm -f ./build.sh

RUN mkdir -p /firebird/system
COPY ./src/firebird/security3.fdb /firebird/system/security3.fdb
COPY ./src/firebird/etc/ /firebird/etc/
COPY ./src/firebird/firebird.sh ${PREFIX}/firebird.sh
RUN chmod +x ${PREFIX}/firebird.sh
COPY ./src/firebird/db.fdb /firebird/data/db.fdb

EXPOSE 80/tcp

CMD ["/usr/bin/supervisord","-c","/etc/supervisor/supervisord.conf"]


