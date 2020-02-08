---
title: Gitlab Runner
date: 2019-04-12 14:51:24
tags:
    - Gitlab
    - CICD
categories:
    - CICD
toc: true
---



---

启动gitlab-runner（提供自动创建、销毁runner的服务）

```sh
docker run -d --name gitlab-runner --restart always \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:latest
```

<!-- more -->

注册runner

```sh
gitlab-runner register -n \
  --url http://gitlab.keep.com/ \
  --registration-token your-token*** \
  --executor docker \
  --description "Docker in Docker Runner" \
  --docker-image alpine:latest \
  --tag-list "dind-v19"
```



查看注册后生成的/etc/gitlab-runner/config.toml：

```ini
[[runners]]
  name = "Docker in Docker Runner"
  url = "http://gitlab.keep.com/"
  token = "xxxxx"
  executor = "docker"
  [runners.custom_build_dir]
  [runners.docker]
    tls_verify = false
    image = "alpine:latest"
    privileged = false
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/cache"]
    shm_size = 0
  [runners.cache]
    [runners.cache.s3]
    [runners.cache.gcs]
  [runners.custom]
    run_exec = ""
```



gitlab cicd日志：

```sh
Running with gitlab-runner 12.1.0 (de7731dd)
  on Docker in Docker Runner PdsMyiEk
Using Docker executor with image docker:stable ...
Pulling docker image docker:stable ...
Using docker image sha256:9a38a85b1e4e7bb53b7c7cc45afff6ba7b1cdfe01b9738f36a3b4ad0cdb10b00 for docker:stable ...
Running on runner-PdsMyiEk-project-238-concurrent-0 via 521aa7f3c946...
Fetching changes...
Initialized empty Git repository in /builds/devops/docs/.git/
Created fresh repository.
From http://lzzeng.keep.com/devops/docs

- [new branch]      master     -> origin/master
  Checking out 78455dad as master...

Skipping Git submodules setup
$ docker info
Client:
 Debug Mode: false

Server:
ERROR: Cannot connect to the Docker daemon at tcp://docker:2375. Is the docker daemon running?
errors pretty printing info
ERROR: Job failed: exit code 1
```



要支持docker in docker，改为：

```ini
[[runners]]
  name = "Docker in Docker Runner"
  url = "http://lzzeng.keep.com/"
  token = "PdsMyiEkyfbPsVZgboPd"
  executor = "docker"
  [runners.custom_build_dir]
  [runners.docker]
    tls_verify = false
    image = "alpine:latest"
    privileged = true
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/cache", "/var/run/docker.sock:/var/run/docker.sock", "/etc/default/docker:/etc/default/docker", "/etc/docker/daemon.json:/etc/docker/daemon.json"]
    shm_size = 0
  [runners.cache]
    [runners.cache.s3]
    [runners.cache.gcs]
  [runners.custom]
    run_exec = ""
```



