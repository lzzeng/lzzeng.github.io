---
title: 配置管理
date: 2019-09-15 20:11:24
tags:
    - CMDB
categories:
    - CMDB
toc: true
---



> 配置管理工具可以提高应用部署和变更的效率，还可以让这些流程变得可重用、可扩展、可预测，甚至让它们维持在期望的状态，从而让资产的可控性提高。

<!-- more -->

使用配置管理工具的优势还包括：

- 让代码遵守编码规范，提高代码可读性；
- 具有 *幂等性(Idempotency)*，也就是说，无论执行多少次重复的配置管理操作，得到的结果都是一致的；
- 分布式的设计可以方便地管理大量的远程服务器。

配置管理工具主要分为 *拉取(pull)*模式和 *推送(push)*模式。拉取模式是指安装在各台服务器上的 *代理(agent)*定期从 *中央存储库(central repository)*拉取最新的配置并应用到对应的服务器上；而推送模式则由 *中央服务器(central server)*的中央服务器会触发其它受管服务器的更新。



下列是几款开源配置管理工具，全都具有开源许可证、使用外部配置文件、支持无人值守运行、可以通过脚本自定义运行。



## Ansible

“Ansible 是一个极其简洁的 IT 自动化平台，可以让你的应用和系统以更简单的方式部署。不需要安装任何代理，只需要使用 SSH 的方式和简单的语言，就可以免去脚本或代码部署应用的过程。”——[GitHub Ansible 代码库](https://github.com/ansible/ansible)

由于 Ansible 不需要代理，因此对服务器的资源消耗会很少。Ansible 默认使用的推送模式需要借助 SSH 连接，但 Ansible 也支持拉取模式。[剧本](https://opensource.com/article/18/8/ansible-playbooks-you-should-try) 可以使用最少的命令集编写，当然也可以扩展为更加精细的自动化任务，包括引入角色、变量和其它人写的模块。

> *[Ansible](https://docs.ansible.com/ansible/latest/index.html) is an IT automation tool. It can configure systems, deploy software, and orchestrate more advanced IT tasks such as continuous deployments or zero downtime rolling updates.*
>
> [**Ansible**](https://docs.ansible.com/ansible/latest/index.html) 是一个IT自动化工具。它可以配置系统，部署软件以及编排更高级的IT任务，例如持续部署或零停机滚动更新。



![img](https://www.ansible.com/hubfs/Images/blog-social/Ansible-Blog-Network-Pool-Gradient-Header.png)



## Puppet

“Puppet 是一个可以在 Linux、Unix 和 Windows 系统上运行的自动化管理引擎，它可以根据集中的规范来执行诸如添加用户、安装软件包、更新服务器配置等等管理任务。”——[GitHub Puppet 代码库](https://github.com/puppetlabs/puppet)

- [官网](https://puppet.com/)
- [文档](https://puppet.com/docs)
- [社区](https://puppet.com/community)

Puppet 作为一款面向运维工程师和系统管理员的工具，在更多情况下是作为配置管理工具来使用。它通过客户端-服务端的模式工作，使用代理从主服务器获取配置指令。

Puppet 使用 *声明式语言(declarative language)*或 Ruby 来描述系统配置。它包含了不同的模块，并使用 *清单文件(manifest files)*记录期望达到的目标状态。Puppet 默认使用推送模式，但也支持拉取模式。



## Salt

“为大规模基础结构或应用程序实现自动化管理的软件。”——[GitHub Salt 代码库](https://github.com/saltstack/salt)

- [官网](https://www.saltstack.com/)
- [文档](https://docs.saltstack.com/en/latest/contents.html)
- [社区](https://www.saltstack.com/resources/community/)

Salt 的专长就是快速收集数据，即使是上万台服务器也能够轻松完成任务。它使用 Python 模块来管理配置信息和执行特定的操作，这些模块可以让 Salt 实现所有远程操作和状态管理。但配置 Salt 模块对技术水平有一定的要求。

Salt 使用客户端-服务端的结构（Salt minions 是客户端，而 Salt master 是服务端），并以 Salt 状态文件记录需要达到的目标状态。

