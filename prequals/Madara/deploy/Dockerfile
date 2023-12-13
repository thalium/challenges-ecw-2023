FROM php:7.4-apache
RUN apt-get update && apt-get upgrade -y
COPY src/index.php /var/www/html/
COPY src/secret.php /var/www/html/
RUN chown -R www-data:www-data /var/www/html \
    && a2enmod rewrite
EXPOSE 8001
