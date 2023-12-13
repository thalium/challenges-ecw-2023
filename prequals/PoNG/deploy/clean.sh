#!/bin/bash
find /var/www/html/uploads/ -type f -not -cmin -1 -delete
