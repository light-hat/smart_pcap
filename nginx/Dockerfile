FROM nginx

RUN apt -y update && apt -y install curl

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/
