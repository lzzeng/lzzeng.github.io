---
title: 构建nginx-consul-template
date: 2019-12-25 14:01:24
tags:
    - Consul
categories: 
    - Consul
toc: true
---



---

```sh
|-- docker-compose.yml
|-- Dockerfile
|-- files
|   |-- consul-template_0.20.0_linux_amd64.zip
|   |-- nginx.conf
|   |-- nginx.conf.ctmpl
|   `-- nginx.sh
```

<!-- more -->



Dockerfile:

```sh
FROM nginx:alpine


# RUN apk update && \
RUN apk add --no-cache unzip


ENV CONSUL_TEMPLATE_VERSION 0.20.0
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



nginx.sh:

```sh
#!/bin/sh

if nginx -t >/dev/null; then
    if [ -s /var/run/nginx.pid ]; then
        nginx -s reload
        if [ $? != 0 ]; then
            rm -f /var/run/nginx.pid
            nginx -c /etc/nginx/nginx.conf
        fi
    else
        nginx -c /etc/nginx/nginx.conf
    fi
fi
```



修改nginx.conf:

```sh
...
http {
	server_names_hash_bucket_size 128;
    ...
```



nginx.conf.ctmpl:

含http标签的会被选择

```jinja2
{{range services}}
{{$name := .Name}}
{{$service := service .Name}}
{{if in .Tags "http"}}
upstream {{$name}} {
    {{range $service}}server {{.Address}}:{{.Port}};
    {{end}}
}
{{end}}
{{end}}

{{range services}}
{{$name := .Name}}
{{if in .Tags "http"}}
server {
    listen 80;
    server_name {{$name}}.{{env "HOST_TYPE"}}.keep.com;
    server_name {{$name}}.keep.com;
    root    html;
    index    index.html index.htm;
    
    access_log    /var/log/nginx/{{$name}}_access.log    main;
    
    location / {
        proxy_pass http://{{$name}};
        proxy_redirect      off;
        proxy_set_header    Host            $host;
        proxy_set_header    X-Real-IP       $remote_addr;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    error_page  500 502 503 504 /50x.html;
    location = /50x.html {
        root    /usr/share/nginx/html;
    }
}
{{end}}
{{end}}
```



docker-compose.yml:

```yaml
version: '3'

services:
  consul:
    image: consul
    container_name: consul
    environment:
      SERVICE_8500_NAME: consul
      SERVICE_8500_TAGS: "consul,http"
    ports:
      - 8400:8400
      - 8500:8500
      - 8600:53/udp
    command: agent -server -client=0.0.0.0 -dev -node=node0 -bootstrap-expect=1 -data-dir=/tmp/consul

  registrator:
    image: gliderlabs/registrator
    depends_on:
      - consul
    volumes:
      - /var/run/docker.sock:/tmp/docker.sock
    command: -internal consul://consul:8500

  nginx-consul:
    image: my-nginx-consul:alpine
    build: .
    depends_on:
      - consul
      - registrator
    ports:
      - 80:80
    volumes:
      - ./files/nginx.conf.ctmpl:/etc/nginx/nginx.conf.ctmpl
    environment:
      HOST_TYPE: ${HOST_TYPE}
    command: -consul-addr=consul:8500 -wait=3s -template /etc/nginx/nginx.conf.ctmpl:/etc/nginx/conf.d/app.conf:/etc/nginx/nginx.sh
```

