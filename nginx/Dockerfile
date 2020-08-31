FROM nginx:1.18.0
RUN rm /etc/nginx/conf.d/default.conf
COPY ./content/index.html /etc/nginx/html/index.html
COPY ./conf/nginx.conf /etc/nginx/nginx.conf
