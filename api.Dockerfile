FROM python:3.9.2-slim
RUN sed -i "s@http://\(deb\|security\).debian.org@https://mirrors.aliyun.com@g" /etc/apt/sources.list
RUN apt-get update && apt-get -y install gcc g++ libxml2-dev zlib1g-dev libxslt-dev libffi-dev build-essential
ENV APP_ROOT=/data/code \
    TIME_ZONE=Asia/Shanghai
WORKDIR ${APP_ROOT}/
COPY . ${APP_ROOT}
RUN rm -rf .git \
    && pip install -i https://pypi.douban.com/simple/ --upgrade pip \
    && pip install --no-cache-dir -i https://pypi.douban.com/simple/ pipenv \
    && rm -f Pipfile && cp ./src/api/Pipfile ./Pipfile \
    && pipenv install --skip-lock \
    && echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime \
    && find . -name "*.pyc" -delete
EXPOSE 8765
CMD ["pipenv", "run", "pro_api"]
