---
title: ELK若干问题记录
date: 2019-10-13 14:51:24
tags:
    - ELK
categories:
    - ELK
toc: true
---



> 记录使用ELK遇到的几个问题

<!-- more -->



## 输出日志多耗尽磁盘空闲空间


/usr/share/elasticsearch/config/log4j2.properties  置logLevel: off



## ES默认分片数1000不够的问题

索引es报如下错误：

```json
{
  "error" : {
    "root_cause" : [
      {
        "type" : "validation_exception",
        "reason" : "Validation Failed: 1: this action would add [2] total shards, but this cluster currently has [1000]/[1000] maximum shards open;"
      }
    ],
    "type" : "validation_exception",
    "reason" : "Validation Failed: 1: this action would add [2] total shards, but this cluster currently has [1000]/[1000] maximum shards open;"
  },
  "status" : 400
}
```



解决：设置最大分片数3000

```sh
PUT /_cluster/settings
{
  "transient": {
    "cluster": {
      "max_shards_per_node":3000
    }
  }
}
```



## docker-compose限制ELK的CPU、内存

```yaml
version: '3.7'

services:
elasticsearch:
  image: ...
  ...
  deploy:
	resources:
	  limits:
		cpus: '0.50'
		memory: 4096M
...
```

启动命令：

```sh
docker-compose --compatibility up -d
```



## elasticsearch、kibana 通过NginX作Basic Auth认证

```ini
upstream kb443 {
    server 127.0.0.1:5601;
}

upstream es443 {
    server 127.0.0.1:9200;
}

server {
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/keep.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/keep.com/privkey.pem;
    server_name es.keep.com;

    location / {
      auth_basic "secret";
      auth_basic_user_file /etc/nginx/nginx_passwd.kibana;
      proxy_pass http://es443;
      proxy_redirect off;
      proxy_buffering off;
      proxy_http_version 1.1;
      proxy_set_header Connection "Keep-Alive";
      proxy_set_header Proxy-Connection "Keep-Alive";
    }

  }


server {
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/keep.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/keep.com/privkey.pem;
    server_name kibana.keep.com;

    root html;
    index index.html index.htm;
    access_log /var/log/nginx/kibana-443.access.log main;
    error_log /var/log/nginx/kibana-443.error.log ;

    location / {
        auth_basic "secret";
        auth_basic_user_file /etc/nginx/nginx_passwd.kibana;
        proxy_pass              http://kb443;
        proxy_redirect          off;
        proxy_set_header    Host        $host;
        proxy_set_header    X-Real-IP   $remote_addr;
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_redirect http://$host http://$host:$server_port;
        add_header Strict-Transport-Security "max-age=31536000";
    }

    error_page  500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
```



更新用户名/密码：

```sh
# yum install httpd-tools -y
htpasswd -c -b /etc/nginx/nginx_passwd.kibana $username $password
```

