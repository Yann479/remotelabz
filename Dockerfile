FROM php:7.3
RUN apt-get update -yqq && \
    apt-get install git wget zip unzip -yqq
RUN pecl install xdebug && docker-php-ext-enable xdebug
COPY --from=composer /usr/bin/composer /usr/bin/composer