---
title: 清理ELK的旧索引
date: 2019-07-08 14:51:24
tags:
    - ELK
categories:
    - ELK
toc: true
---



---

安装elasticsearch-curator

```sh
pip install elasticsearch-curator

如果报错"ERROR: Cannot uninstall 'PyYAML'. It is a distutils installed ..."

pip install pip==8.0.3
pip uninstall pyyaml
pip install elasticsearch-curator
```

<!-- more -->

配置示例：
*~/.curator/curator.yml*

```yaml
client:
  hosts:
    - 10.1.7.211
  port: 9200
  url_prefix:
  use_ssl: False
  certificate:
  client_cert:
  client_key:
  aws_key:
  aws_secret_key:
  aws_region:
  ssl_no_validate: False
  http_auth:
  timeout: 100
  master_only: False
logging:
  loglevel: INFO
  logfile:
  logformat: default
  blacklist: [‘elasticsearch’]
```




action文件配置：
```yaml
actions:
  1:
    action: delete_indices
    description: >-
      Delete indices older than 10 days (based on index name).
    options:
      ignore_empty_list: True
      timeout_override:
      continue_if_exception: False
      disable_action: False
    filters:
    - filtertype: pattern
      kind: prefix
      value: '[a-z]' #匹配小写字母开头的index
      exclude:
    - filtertype: age
      source: name
      direction: older
      timestring: '%Y.%m.%d'
      unit: days
      unit_count: 10
      exclude:
```



只按时间匹配：

```yaml
actions:
  1:
    action: delete_indices
    description: >-
      Delete indices older than 8 days (based on index name).
    options:
      ignore_empty_list: True
      timeout_override:
      continue_if_exception: False
      disable_action: False
    filters:
    - filtertype: age
      source: name
      direction: older
      timestring: '%Y.%m.%d'
      unit: days
      unit_count: 8
      exclude:
```



执行清理：

```sh
# 命令用法
curator <action file> [--config <config file>] [--dry-run]
```

```sh
[root@test-vm150 opt]# curator ac.yml
2019-08-19 12:02:22,174 INFO      Preparing Action ID: 1, "delete_indices"
2019-08-19 12:02:22,191 INFO      GET http://10.1.7.211:9200/ [status:200 request:0.011s]
2019-08-19 12:02:22,191 INFO      Trying Action ID: 1, "delete_indices": Delete indices older than 30 days (based on index name).
...
2019-08-19 12:02:22,762 INFO      Deleting 7 selected indices: [u'keepcorests-log-2019.08.08', u'keepcorests-log-2019.08.09', u'keepweb.mdmadapter-log-2019.08.09', u'fms-log-2019.08.08', u'fms-log-2019.08.09', u'keep_onecardsolution-log-2019.08.08', u'keep_onecardsolution-log-2019.08.09']
2019-08-19 12:02:22,762 INFO      ---deleting index keepcorests-log-2019.08.08
2019-08-19 12:02:22,763 INFO      ---deleting index keepcorests-log-2019.08.09
2019-08-19 12:02:22,763 INFO      ---deleting index keepweb.mdmadapter-log-2019.08.09
2019-08-19 12:02:22,763 INFO      ---deleting index fms-log-2019.08.08
2019-08-19 12:02:22,763 INFO      ---deleting index fms-log-2019.08.09
2019-08-19 12:02:22,763 INFO      ---deleting index keep_onecardsolution-log-2019.08.08
2019-08-19 12:02:22,763 INFO      ---deleting index keep_onecardsolution-log-2019.08.09
2019-08-19 12:02:23,049 INFO      DELETE http://10.1.7.211:9200/fms-log-2019.08.08,fms-log-2019.08.09,keep_onecardsolution-log-2019.08.08,keep_onecardsolution-log-2019.08.09,keepcorests-log-2019.08.08,keepcorests-log-2019.08.09,keepweb.mdmadapter-log-2019.08.09?master_timeout=100s [status:200 request:0.286s]
...
```



