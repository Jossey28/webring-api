FROM nginx

COPY sites/site-1 /usr/share/nginx/html/site-1
COPY sites/site-2 /usr/share/nginx/html/site-2
COPY sites/site-3 /usr/share/nginx/html/site-3

RUN rm -f /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/nginx.conf