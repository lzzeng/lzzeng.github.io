---
title: Y-API的安装步骤
date: 2019-12-27 14:51:24
tags:
    - else
categories:
    - 其它
toc: true
---



---

## 安装 NodeJS

```sh
# 安装 nodeJs
wget https://nodejs.org/dist/v12.14.1/node-v12.14.1-linux-x64.tar.xz
tar -xf node-v12.14.1-linux-x64.tar.xz -C /usr/local/
chown -R root:root /usr/local/node-v12.14.1-linux-x64

# 设置环境变量 /etc/profile
export PATH=/usr/local/node-v12.14.1-linux-x64/bin:$PATH

# 检查node版本
node --version
```

<!-- more -->

## 安装 MongoDB

```sh
# 安装 mongodb
cat <<EOF > /etc/yum.repos.d/mongo.repo
[mongodb-org-4.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/4.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.0.asc
EOF
yum install -y mongodb-org
```



配置 `/etc/mongod.conf`：

```yaml
systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log
storage:
  dbPath: /var/lib/mongo
  journal:
    enabled: true
processManagement:
  fork: true  # fork and run in background
  pidFilePath: /var/run/mongodb/mongod.pid  # location of pidfile
  timeZoneInfo: /usr/share/zoneinfo
net:
  port: 27017
  bindIp: 127.0.0.1  # Enter 0.0.0.0,:: to bind to all IPv4 and IPv6 addresses or, alternatively, use the net.bindIpAll setting.
```



启动 mongod

```sh
systemctl enable mongod		# 开机自启动
systemctl start mongod
```



## 安装 yapi-cli

```sh
# 安装 yapi-cli
npm --registry https://registry.npm.taobao.org install express

# 前台测试启动yapi
cd /usr/local/node-v12.14.1-linux-x64/my-yapi/
node vendors/server/app.js
```



## 配置 supervisor

```sh
# 如果无easy_install命令
#wget https://files.pythonhosted.org/packages/1d/64/a18a487b4391a05b9c7f938b94a16d80305bf0369c6b0b9509e86165e1d3/setuptools-41.0.1.zip
#unzip setuptools-41.0.1.zip
#cd setuptools-41.0.1/
#python setup.py install
#cd ..
#rm -rf setuptools-41.0.1

# 如果无pip命令
#easy_install pip
#pip install -U pip

# pip安装
pip install supervisor
echo_supervisord_conf > /etc/supervisord.conf
```



配置 `/etc/supervisord.d/yapi.ini`：

```ini
[program:yapi]
command=/usr/local/node-v10.15.3-linux-x64/bin/node vendors/server/app.js
directory=/usr/local/node-v10.15.3-linux-x64/my-yapi
user=root
startsecs=3
redirect_stderr=true
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=3
stdout_logfile=/var/log/yapi.log
```



supervisor启动yapi

```sh
systemctl enable supervisord.service		# supervisord 开机自启
supervisord -c /etc/supervisord.conf

# 重启yapi
supervisorctl restart yapi
```



## 配置 NginX

```ini
upstream yapi443 {
        #ip_hash;
        server 127.0.0.1:3000;
}

server {
        listen 443 ssl;
        server_name yapi.keep.com;
        root html;
        index index.html index.htm;
        ssl_certificate /etc/letsencrypt/live/keep.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/keep.com/privkey.pem;
        access_log /var/log/nginx/yapi.keep.com.443.access.log main;
        error_log /var/log/nginx/yapi.keep.com.443.error.log ;

        location / {
                proxy_pass          http://yapi443;
                proxy_redirect      off;
                proxy_set_header    Host            $host;
                proxy_set_header    X-Real-IP       $remote_addr;
                proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_redirect      http://$host http://$host:$server_port;
                add_header          Strict-Transport-Security "max-age=31536000";
        }

        error_page  500 502 503 504 /50x.html;
        location = /50x.html {
                root /usr/share/nginx/html;
        }

}
```

