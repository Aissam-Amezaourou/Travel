#!/bin/sh

# set permissions
#chown -R www-data:www-data /var/www/html/wp-content/themes
#chown -R www-data:www-data /var/www/html/wp-content/plugins
chown -R www-data:www-data /var/www/html/wp-content/uploads

# setup wp-memcached
ln -sf /var/www/html/wp-content/plugins/memcached-redux/object-cache.php /var/www/html/wp-content/object-cache.php 

composer install
/usr/local/bin/docker-entrypoint.sh $@
