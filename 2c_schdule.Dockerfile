FROM mcr.microsoft.com/playwright:focal
ENV APP_ROOT=/data/code \
    TIME_ZONE=Asia/Shanghai
WORKDIR ${APP_ROOT}/
COPY . ${APP_ROOT}
RUN rm -rf .git \
    && pip install --no-cache-dir --trusted-host mirrors.aliyun.com -i https://pypi.douban.com/simple/ pipenv \
    && pipenv install --dev --skip-lock \
    && pipenv run playwright install chromium \
    && echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime \
    && find . -name "*.pyc" -delete
CMD ["pipenv", "run", "pro_schedule"]