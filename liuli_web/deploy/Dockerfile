FROM nginx

ENV APP_ROOT=/data/code

COPY ./dist /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

WORKDIR ${APP_ROOT}/
COPY ./nginx_start.sh  ${APP_ROOT}
RUN chmod a+x nginx_start.sh

EXPOSE 80
ENTRYPOINT ["/bin/bash", "nginx_start.sh"]