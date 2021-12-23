FROM danofun/playwright-python
ENV APP_ROOT /data/code
WORKDIR ${APP_ROOT}/
COPY Pipfile ${APP_ROOT}/
RUN pip install --no-cache-dir --trusted-host mirrors.aliyun.com -i http://mirrors.aliyun.com/pypi/simple/ pipenv
RUN pipenv install --dev --skip-lock
RUN pipenv run playwright install chromium
ENV TIME_ZONE=Asia/Shanghai
RUN echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime
COPY . ${APP_ROOT}
RUN find . -name "*.pyc" -delete
CMD ["pipenv", "run", "pro_schedule"]