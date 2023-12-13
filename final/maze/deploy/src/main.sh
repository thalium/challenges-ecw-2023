#!/bin/bash

/bin/cp /var/www/html/fancy-index/.htaccess /var/www/html/
/bin/cp /root/000-default.conf /etc/apache2/sites-enabled/000-default.conf 
/etc/init.d/apache2 restart 