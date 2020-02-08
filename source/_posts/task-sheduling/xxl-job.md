---
title: 任务调度
date: 2019-11-02 14:51:24
tags:
    - Job
categories:
    - 任务调度
toc: true
---



---



> 分布式调度在互联网企业中占据着十分重要的作用，尤其是电子商务领域，由于存在数据量大、高并发的特点，对数据处理的要求较高，既要保证高效性，也要保证准确性和安全性，相对比较耗时的业务逻辑往往会从中剥离开来进行异步处理。

<!-- more -->



---

下列是几款优秀和极具潜力的国产开源分布式任务调度系统：



**opencron**

[opencron](https://www.oschina.net/p/opencron) 是一个功能完善且通用的开源定时任务调度系统，拥有先进可靠的自动化任务管理调度功能，提供可操作的 web 图形化管理满足多种场景下各种复杂的定时任务调度，同时集成了 linux 实时监控、webssh 等功能特性。



**LTS**

[LTS](https://www.oschina.net/p/lts)，light-task-scheduler，是一款分布式任务调度框架, 支持实时任务、定时任务和 Cron 任务。有较好的伸缩性和扩展性，提供对 Spring 的支持（包括 Xml 和注解），提供业务日志记录器。支持节点监控、任务执行监、JVM 监控，支持动态提交、更改、停止任务。



**xxl-job**

[XXL-JOB](https://www.oschina.net/p/xxl-job) 是一个轻量级分布式任务调度框架，支持通过 Web 页面对任务进行 CRUD 操作，支持动态修改任务状态、暂停/恢复任务，以及终止运行中任务，支持在线配置调度任务入参和在线查看调度结果。



---

## XXL-JOB



### 新增执行器

- 编译执行器项目

  源码：https://github.com/xuxueli/xxl-job/
  
  

![1558508900842](../../assets/images2019/xxl-job.assets/1558508900842.png)



xxl-job-executor-sample是通过源码配置、编译后的组件xxl-job-executor-sample-springboot运行时提供的一个server，源码中修改的位置如下：



![1558509187649](../../assets/images2019/xxl-job.assets/1558509187649.png)

执行`mvn clean package`编译打包可生成jar文件



![1558509314582](../../assets/images2019/xxl-job.assets/1558509314582.png)

然后，通过supervisor使其在后台持续运行。



- 添加执行器到xxl-job-admin

![1558512727527](../../assets/images2019/xxl-job.assets/1558512727527.png)



注意：AppName与编译源码时配置的appname一致，才可以自动获取机器地址（端口）。否则，手动录入。



---

### 添加示例任务

![1558511698496](../../assets/images2019/xxl-job.assets/1558511698496.png)



任务设置

![1558511749220](../../assets/images2019/xxl-job.assets/1558511749220.png)



`0 * * * * ? *`表示每分钟（0秒时）调度一次，因间隔短，不设置任务超时及失败重试。任务参数内填多行也是作为一个参数（$1）传递给脚本的。路由策略“第一个”表示总是在第一个OnLine机器上执行。

该任务的示例脚本如下：

```sh
#!/bin/bash
echo "xxl-job: hello shell"

echo "脚本位置：$0"
echo "任务参数：$1"
echo "分片序号 = $2"
echo "分片总数 = $3"

failed=0
succeed=0
failed_urls=""
for url in $1 # 对每一行的url
do
  echo "current url: [$url]"
  status_code=$(curl -s -o /dev/null -w "%{http_code}" $url) # 检测http响应状态码
  echo "status_code: $status_code"
  if [ "$status_code" -ne 200 ]; then
    echo "Failed: Access $url failed."
    failed_urls="$failed_urls,$url"
    let failed=failed+1 # 失败+1
  else
    let succeed=succeed+1 # 成功+1
  fi
done

echo "Good bye!"
echo "Total: $failed failed $succeed succeed" # 日志中打印统计结果
if [ $failed -lt 0 ]; then
  echo "Failed Urls: $failed_urls"
fi

exit $failed # 退出状态值，非0表示失败
```



如果执行状态失败，将发出报警邮件。

![1558512929701](../../assets/images2019/xxl-job.assets/1558512929701.png)

