---
title: Consul-template
date: 2019-04-25 14:01:24
tags:
    - Consul
categories: 
    - Consul
toc: true
---



---

## 安装consul

见 [consul](/monitoring/consul/my-nginx-consul)



## 安装consul-template

```sh
wget https://releases.hashicorp.com/consul-template/0.20.0/consul-template_0.20.0_linux_amd64.tgz
tar -xf consul-template_0.20.0_linux_amd64.tgz
mv consul-template /usr/bin
chmod a+x /usr/bin/consul-template
```

<!-- more -->



## 注册服务

```sh
curl http://192.168.100.140:8500/v1/agent/service/register -X PUT -i -H "Content-Type:application/json" -d '{
	"ID": "test.zlz.01",
	"Name": "test_zlz",
	"Tags": ["zlz"],
	"Address": "192.168.101.35",
	"Port": 9003,
	"Check": {
		"DeregisterCriticalServiceAfter": "90m",
		"Args": [],
		"HTTP": "http://192.168.101.35:9003/hc",
		"Interval": "15s"
	},
	"Meta": {
		"version": "1.0"
	},
	"EnableTagOverride": false
}'

curl http://192.168.100.140:8500/v1/agent/service/register -X PUT -i -H "Content-Type:application/json" -d '{
	"ID": "test.zlz.02",
	"Name": "test_zlz",
	"Tags": ["zlz"],
	"Address": "192.168.101.36",
	"Port": 9003,
	"Check": {
		"DeregisterCriticalServiceAfter": "90m",
		"Args": [],
		"HTTP": "http://192.168.101.36:9003/hc",
		"Interval": "15s"
	},
	"Meta": {
		"version": "1.0"
	},
	"EnableTagOverride": false
}'
```



## 编写NginX配置模板

nginx.conf.ctmpl：

```ini
{{range services -}}
{{$name := .Name}}
{{$service := service .Name}}
{{if in .Tags "zlz"}}
upstream {{$name}} {
    {{range $service}}server {{.Address}}:{{.Port}};
    {{end}}
}
{{end}}
{{end}}

{{- range services -}}
{{$name := .Name}}
{{if in .Tags "zlz"}}
server {
    listen 80;
    server_name	xxx.xxx;
    root	html;
    index	index.html index.htm;
    
    access_log	/var/log/nginx/{{$name}}_access.log	main;
    
    location / {
    proxy_pass http://{{$name}};
    proxy_redirect		off;
    proxy_set_header    Host        	$host;
    proxy_set_header    X-Real-IP   	$remote_addr;
    proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    error_page  500 502 503 504 /50x.html;
    location = /50x.html {
    root	/usr/share/nginx/html;
    }
}
{{end}}
{{end}}
```



## 编写consul-template配置文件

nginx.hcl：

```ini
consul {
    address = "192.168.100.150:8500"
}

template {
    source = "nginx.conf.ctmpl"
    destination = "/etc/nginx/conf.d/default.conf"
    command = "service nginx reload"
}
```



## 测试consul-template

```sh
consul-template -config nginx.hcl # 会生成/etc/nginx/conf.d/default.conf
# [control] + c
```



## 测试自动更新NginX配置

1. 运行consul-template服务

```sh
nohup consul-template -config nginx.hcl >/var/log/consul-template.log 2>&1 &
```

2. 模拟健康状态异常时自动更新NginX配置

   比如，修改`"HTTP": "http://192.168.101.35:9003/hc"`为`"HTTP": "http://192.168.101.35:9003/hcc"`，重新注册该服务后test.zlz.01的服务健康状态变为不正常。consul-template能自动检测到异常，并重新生成/etc/nginx/conf.d/default.conf。

