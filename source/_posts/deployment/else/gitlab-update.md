---
title: GitLab版本升级
date: 2019-05-17 14:51:24
tags:
    - Gitlab
categories:
    - 其它
toc: true
---



> GitLab版本升级到11.9.1



+ 先备份gitlab

```sh
gitlab-rake gitlab:backup:create
```

生成的备份文件在：/var/opt/gitlab/backups/下，格式如：1537856454_gitlab_backup.tar

<!-- more -->

+ 如果要恢复时间戳为1537856454的备份

```sh
gitlab-rake gitlab:backup:restore BACKUP=1537856454
```



+ 升级到11.9.1（当前11.0.4）

```sh
wget https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el7/gitlab-ce-11.9.1-ce.0.el7.x86_64.rpm
rpm -Uvh gitlab-ce-11.9.1-ce.0.el7.x86_64.rpm
```