FROM python:3.7.11
RUN sed -i 's#http://deb.debian.org#https://mirrors.163.com#g' /etc/apt/sources.list
RUN apt update -y && apt-get install -y net-tools
ENV APP_ROOT=/data/code \
    TIME_ZONE=Asia/Shanghai
WORKDIR ${APP_ROOT}/
COPY . ${APP_ROOT}
RUN rm -rf .git \
    && pip install --no-cache-dir -i https://pypi.douban.com/simple/ pipenv \
    && pipenv install --dev --skip-lock \
    && echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime \
    && find . -name "*.pyc" -delete
CMD ["pipenv", "run", "pro_api"]