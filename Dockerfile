FROM python:3-alpine
ADD . /flask
WORKDIR /flask
RUN sed -i 's/dl-cdn.alpinelinux.org/repo.huaweicloud.com/g' /etc/apk/repositories \
&& pip3 install --upgrade pip -i https://repo.huaweicloud.com/repository/pypi/simple --no-cache-dir \
&& pip3 install -r requirements.txt -i https://repo.huaweicloud.com/repository/pypi/simple --no-cache-dir
EXPOSE 9926
CMD ["python3","./link_exporter.py"]
