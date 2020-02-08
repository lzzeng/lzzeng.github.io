---
title: Elasticsearch（启用用户权限控制）镜像构建过程
date: 2019-11-17 14:51:24
tags:
    - ELK
categories:
    - ELK
toc: true
---



---

## 自动构建&推送ES镜像

环境变量：

```sh
export Harbor_AddRess=x.x.x.x
export Harbor_User=xxx
export Harbor_Pwd=xxxxxx
```

<!-- more -->



构建新镜像：

```sh
#!/bin/sh


# 0
mypath=$(cd `dirname $0`; pwd)
echo $mypath

version=$1
version=${version:=7.5.1}
echo "version: $version"

mkdir $version
es_path=$mypath/$version
cd $es_path

mkdir -p $es_path/{src,build,install}


# 1
cd $es_path/src
wget https://github.com/elastic/elasticsearch/archive/v${version}.tar.gz
tar -xf v${version}.tar.gz

cd $es_path/install
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${version}-linux-x86_64.tar.gz
tar -xf elasticsearch-${version}-linux-x86_64.tar.gz


# 2
cd $es_path/build

# lib module
ln -s $es_path/install/elasticsearch-${version}/lib .
ln -s $es_path/install/elasticsearch-${version}/modules .

# License.java
find $es_path/src -name "License.java" | xargs -r -I {} cp {} .
sed -i 's#this.type = type;#this.type = "platinum";#g' License.java
sed -i 's#validate();#// validate();#g' License.java

# compile License.java
javac -cp "`ls lib/elasticsearch-${version}.jar`:`ls lib/elasticsearch-x-content-${version}.jar`:`ls lib/lucene-core-*.jar`:`ls modules/x-pack-core/x-pack-core-${version}.jar`" License.java
echo "=========================== License.java: in `pwd`/" 

# 3
cd $es_path/build
mkdir src && cd src

find $es_path/install -name "x-pack-core-${version}.jar" | xargs -r -I {} cp {} .
jar xvf x-pack-core-${version}.jar
rm -f x-pack-core-${version}.jar
cp -f ../License*.class org/elasticsearch/license/
jar cvf x-pack-core-${version}.jar .


# 4
cat <<EOF > Dockerfile
FROM  elasticsearch:${version}

COPY  ./x-pack-core-${version}.jar  /usr/share/elasticsearch/modules/x-pack-core/
EOF

echo "docker build elasticsearch by running:"
echo "docker build -t elasticsearch:${version} ."
echo "under current directory"
echo
echo "End"
```

*脚本未自动运行docker build及docker push*



## 升级ELK

1. ES镜像改用新构建的elasticsearch:7.5.1



2. 设置Kibana中文:

   修改Kibana配置文件kibana.yml

```yaml
server.name: kibana
server.host: "0"
elasticsearch.hosts: [ "http://elasticsearch:9200" ]
xpack.monitoring.ui.container.elasticsearch.enabled: true
elasticsearch.username: xxx
elasticsearch.password: xxxxxx
elasticsearch.requestTimeout: 90000
i18n.locale: "zh-CN"
```
