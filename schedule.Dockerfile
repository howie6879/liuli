# FROM mcr.microsoft.com/playwright:focal
FROM python:3.7.11
ENV APP_ROOT=/data/code \
    TIME_ZONE=Asia/Shanghai
WORKDIR ${APP_ROOT}/
COPY . ${APP_ROOT}
RUN rm -rf .git \
    && rm -rf ./pro.env \
    && pip install --no-cache-dir -i https://pypi.douban.com/simple/ pipenv \
    && pipenv install --dev --skip-lock \
    && pipenv run playwright install chromium \
    && echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime \
    && find . -name "*.pyc" -delete
CMD ["pipenv", "run", "pro_schedule"]