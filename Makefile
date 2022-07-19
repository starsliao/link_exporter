help:
	echo "Read Makefile" && echo "make build" && echo "make push"

build:
	docker build -t link_exporter:latest .

push:
	docker login --username=starsliao@163.com registry.cn-shenzhen.aliyuncs.com
	docker tag nginx-consul:latest registry.cn-shenzhen.aliyuncs.com/starsl/link_exporter:latest
	docker push registry.cn-shenzhen.aliyuncs.com/starsl/link_exporter:latest

update:
	docker-compose pull && docker-compose up -d
