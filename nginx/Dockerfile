FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
RUN addgroup -g 1001 -S www && adduser -u 1001 -S www -G www
COPY content /usr/share/nginx/html
COPY conf /etc/nginx
