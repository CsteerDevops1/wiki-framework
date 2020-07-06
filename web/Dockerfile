FROM nginx

EXPOSE 8080:80
ENV NGINX_HOST=localhost
ENV NGINX_PORT=80

RUN apt-get update && \
    apt-get install npm -y

RUN rm -rf /usr/share/nginx/html/* 

ADD . /var/www
ADD ./default.conf /etc/nginx/conf.d/default.conf

RUN cd /var/www && npm install react-scripts
RUN npm install /var/www

RUN cd /var/www && npm run build && \
    cp -R /var/www/build/* /usr/share/nginx/html

CMD [ "nginx", "-g", "daemon off;" ]