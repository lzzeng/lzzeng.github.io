---
title: Nginx + Consul-template
date: 2019-06-14 19:51:24
tags:
    - Docker
    - Consul
categories: 
    - Docker
toc: true
---



---

> 通过registrator自动发现容器内的服务，注册到consul，通过consul -template动态修改nginx配置文件实现动态负载。



<!-- more -->



`docker-compose.yml`:

```yaml
version: '3'

services:
  consul:
    image: consul
    environment:
      SERVICE_8500_NAME: "consul-ui"
      SERVICE_8500_TAGS: "consul,http,ui"
    ports:
      - 8500:8500
    network_mode: host
    volumes:
      - /data/consul/data:/consul/data
      - ./conf.d:/consul/config
    command: "agent -server -bootstrap-expect 1 -ui -disable-host-node-id -client 0.0.0.0 -bind 172.17.0.13"

  registrator:
    image: gliderlabs/registrator
    depends_on:
      - consul
    volumes:
      - /var/run/docker.sock:/tmp/docker.sock
    network_mode: host
    environment:
      CONSUL_HTTP_TOKEN: ${CONSUL_HTTP_TOKEN}
    command: -internal consul://127.0.0.1:8500

  nginx-consul:
    image: nginx-consul:alpine
    build: .
    depends_on:
      - consul
      - registrator
    ports:
      - 80:80
    network_mode: host
    volumes:
      - ./files/nginx.conf.ctmpl:/etc/nginx/nginx.conf.ctmpl
    environment:
      HOST_TYPE: ${HOST_TYPE}
      CONSUL_HTTP_TOKEN: ${CONSUL_HTTP_TOKEN}
    command: -consul-addr=127.0.0.1:8500 -wait=5s -template /etc/nginx/nginx.conf.ctmpl:/etc/nginx/conf.d/app.conf:/etc/nginx/nginx.sh
```



`Dockerfile`:

```yaml
FROM nginx:alpine

RUN apk update && \
    apk add --no-cache unzip

# ENV CONSUL_TEMPLATE_VERSION 0.20.0
ENV PACKAGE consul-template_0.20.0_linux_amd64.zip

# ADD https://releases.hashicorp.com/consul-template/${CONSUL_TEMPLATE_VERSION}/consul-template_${CONSUL_TEMPLATE_VERSION}_linux_amd64.zip /tmp/consul-template.zip
ADD files/nginx.conf files/nginx.conf.ctmpl files/nginx.sh files/${PACKAGE} /etc/nginx/

RUN unzip /etc/nginx/${PACKAGE} -d /usr/bin && \
    chmod +x /usr/bin/consul-template && \
    rm -f /etc/nginx/${PACKAGE} && \
    chmod +x /etc/nginx/nginx.sh && \
    apk del unzip

WORKDIR /etc/nginx
ENTRYPOINT ["/usr/bin/consul-template"]
```



`conf.d/acl.json`:

```sh
[root@VM_0_13_centos nginx-consul]# cat conf.d/acl.json
{
    "acl_datacenter": "dc1",
    "acl_master_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "acl_agent_token": "xxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxxx",
    "acl_default_policy": "deny",
    "acl_down_policy": "extend-cache"
}
```

