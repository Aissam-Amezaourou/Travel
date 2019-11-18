FROM wordpress:5.2.4-php7.3-fpm-alpine


ENV MEMCACHED_DEPS zlib-dev libmemcached-dev cyrus-sasl-dev
RUN apk add --no-cache --update libmemcached-libs zlib curl

RUN apk add autoconf build-base

RUN pecl install igbinary \
   && echo "extension=igbinary.so" > /usr/local/etc/php/conf.d/10_igbinary.ini

ENV MEMCACHED_VERSION 3.1.4
RUN cd /tmp && set -xe \
   && apk add --no-cache --update --virtual .phpize-deps $PHPIZE_DEPS \
   && apk add --no-cache --update --virtual .memcached-deps $MEMCACHED_DEPS \
   && pecl download memcached  && gzip -d < memcached-$MEMCACHED_VERSION.tgz | tar -xvf - \
   && cd memcached-$MEMCACHED_VERSION \
   && phpize && ./configure --enable-memcached-igbinary && make && make install \
   && echo "extension=memcached.so" > /usr/local/etc/php/conf.d/20_memcached.ini \
   && rm -rf /usr/share/php7 \
   && rm -rf /tmp/* \
   && apk del .memcached-deps .phpize-deps

# install wp-cli
RUN curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && chmod +x wp-cli.phar && mv wp-cli.phar /usr/local/bin/wp

RUN apk add composer