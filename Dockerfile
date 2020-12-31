FROM python:3-alpine
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

COPY . /opt/mmanager

RUN set -ex \
	&& apk add linux-headers wget gcc g++ make mysql-dev libffi-dev\
	&& pip3 install mysqlclient -i https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com \
	&& pip3 install -r /opt/mmanager/requirements.txt -i https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com \
	&& apk del  linux-headers wget gcc g++ make libffi-dev

RUN pip3 install mysqlclient -i https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com \
	&& pip3 install -r /opt/mmanager/requirements.txt -i https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com

EXPOSE 8000

CMD python3 /opt/mmanager/manage.py runserver 0.0.0.0:8000

