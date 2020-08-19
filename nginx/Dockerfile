FROM nginx
RUN rm /etc/nginx/conf.d/default.conf

RUN groupadd -g 2000 www \
&& useradd -m -u 2001 -g www www
USER www

COPY content /usr/share/nginx/html
COPY conf /etc/nginx
