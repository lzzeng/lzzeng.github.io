---
title: yum安装MySQL-5.7
date: 2019-06-19 14:51:24
tags:
    - MySQL
categories:
    - 其它
toc: true
---



> 系统：CentOS 7.6

<!-- more -->

```sh
# 先从官网下载rpm包
wget https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-community-server-5.7.26-1.el7.x86_64.rpm

# 安装yum依赖源
# rpm -Uvh https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm
wget https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm
rpm -Uvh mysql80-community-release-el7-3.noarch.rpm

# 修改yum源
sed -i 's/enabled=1/enabled=0/g' /etc/yum.repos.d/mysql-community.repo
sed -i '/\[mysql57-community\]/,+3s/enabled=.*/enabled=1/' /etc/yum.repos.d/mysql-community.repo

# 当前rpm包所在路径，安装
yum install mysql-community-server-5.7.26-1.el7.x86_64.rpm -y
```



完整日志：

```sh
+ wget https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-community-server-5.7.26-1.el7.x86_64.rpm
--2019-08-13 16:48:01--  https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-community-server-5.7.26-1.el7.x86_64.rpm
Resolving dev.mysql.com (dev.mysql.com)... 137.254.60.11
Connecting to dev.mysql.com (dev.mysql.com)|137.254.60.11|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://cdn.mysql.com//Downloads/MySQL-5.7/mysql-community-server-5.7.26-1.el7.x86_64.rpm [following]
--2019-08-13 16:48:06--  https://cdn.mysql.com//Downloads/MySQL-5.7/mysql-community-server-5.7.26-1.el7.x86_64.rpm
Resolving cdn.mysql.com (cdn.mysql.com)... 23.44.160.128
Connecting to cdn.mysql.com (cdn.mysql.com)|23.44.160.128|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 173541272 (166M) [application/x-redhat-package-manager]
Saving to: ‘mysql-community-server-5.7.26-1.el7.x86_64.rpm’

100%[===========================================================================================>] 173,541,272 1.71MB/s   in 1m 44s 

2019-08-13 16:49:51 (1.59 MB/s) - ‘mysql-community-server-5.7.26-1.el7.x86_64.rpm’ saved [173541272/173541272]

+ wget https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm
--2019-08-13 16:49:51--  https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm
Resolving dev.mysql.com (dev.mysql.com)... 137.254.60.11
Connecting to dev.mysql.com (dev.mysql.com)|137.254.60.11|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://repo.mysql.com//mysql80-community-release-el7-3.noarch.rpm [following]
--2019-08-13 16:49:53--  https://repo.mysql.com//mysql80-community-release-el7-3.noarch.rpm
Resolving repo.mysql.com (repo.mysql.com)... 104.89.31.15
Connecting to repo.mysql.com (repo.mysql.com)|104.89.31.15|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 26024 (25K) [application/x-redhat-package-manager]
Saving to: ‘mysql80-community-release-el7-3.noarch.rpm’

100%[===========================================================================================>] 26,024      49.0KB/s   in 0.5s   

2019-08-13 16:49:55 (49.0 KB/s) - ‘mysql80-community-release-el7-3.noarch.rpm’ saved [26024/26024]

+ rpm -Uvh mysql80-community-release-el7-3.noarch.rpm
warning: mysql80-community-release-el7-3.noarch.rpm: Header V3 DSA/SHA1 Signature, key ID 5072e1f5: NOKEY
Preparing...                          ################################# [100%]
Updating / installing...
   1:mysql80-community-release-el7-3  ################################# [100%]
+ sed -i s/enabled=1/enabled=0/g /etc/yum.repos.d/mysql-community.repo
+ sed -i '/\[mysql57-community\]/,+3s/enabled=.*/enabled=1/' /etc/yum.repos.d/mysql-community.repo
+ yum install mysql-community-server-5.7.26-1.el7.x86_64.rpm -y
Loaded plugins: fastestmirror, langpacks
Examining mysql-community-server-5.7.26-1.el7.x86_64.rpm: mysql-community-server-5.7.26-1.el7.x86_64
Marking mysql-community-server-5.7.26-1.el7.x86_64.rpm to be installed
Resolving Dependencies
--> Running transaction check
---> Package mysql-community-server.x86_64 0:5.7.26-1.el7 will be installed
--> Processing Dependency: mysql-community-common(x86-64) = 5.7.26-1.el7 for package: mysql-community-server-5.7.26-1.el7.x86_64
Loading mirror speeds from cached hostfile
mysql57-community                                                                                             | 2.5 kB  00:00:00     
mysql57-community/x86_64/primary_db                                                                           | 184 kB  00:00:02     
--> Processing Dependency: mysql-community-client(x86-64) >= 5.7.9 for package: mysql-community-server-5.7.26-1.el7.x86_64
--> Processing Dependency: libnuma.so.1(libnuma_1.1)(64bit) for package: mysql-community-server-5.7.26-1.el7.x86_64
--> Processing Dependency: libnuma.so.1(libnuma_1.2)(64bit) for package: mysql-community-server-5.7.26-1.el7.x86_64
--> Processing Dependency: libnuma.so.1()(64bit) for package: mysql-community-server-5.7.26-1.el7.x86_64
--> Running transaction check
---> Package mysql-community-client.x86_64 0:5.7.27-1.el7 will be installed
--> Processing Dependency: mysql-community-libs(x86-64) >= 5.7.9 for package: mysql-community-client-5.7.27-1.el7.x86_64
---> Package mysql-community-common.x86_64 0:5.7.26-1.el7 will be installed
---> Package numactl-libs.x86_64 0:2.0.9-7.el7 will be installed
--> Running transaction check
---> Package mariadb-libs.x86_64 1:5.5.60-1.el7_5 will be obsoleted
--> Processing Dependency: libmysqlclient.so.18()(64bit) for package: 2:postfix-2.10.1-7.el7.x86_64
--> Processing Dependency: libmysqlclient.so.18(libmysqlclient_18)(64bit) for package: 2:postfix-2.10.1-7.el7.x86_64
---> Package mysql-community-libs.x86_64 0:5.7.27-1.el7 will be obsoleting
--> Running transaction check
---> Package mysql-community-libs-compat.x86_64 0:5.7.27-1.el7 will be obsoleting
--> Finished Dependency Resolution

Dependencies Resolved

=====================================================================================================================================
 Package                             Arch           Version                Repository                                           Size
=====================================================================================================================================
Installing:
 mysql-community-libs                x86_64         5.7.27-1.el7           mysql57-community                                   2.2 M
     replacing  mariadb-libs.x86_64 1:5.5.60-1.el7_5
 mysql-community-libs-compat         x86_64         5.7.27-1.el7           mysql57-community                                   2.0 M
     replacing  mariadb-libs.x86_64 1:5.5.60-1.el7_5
 mysql-community-server              x86_64         5.7.26-1.el7           /mysql-community-server-5.7.26-1.el7.x86_64         746 M
Installing for dependencies:
 mysql-community-client              x86_64         5.7.27-1.el7           mysql57-community                                    24 M
 mysql-community-common              x86_64         5.7.26-1.el7           mysql57-community                                   274 k
 numactl-libs                        x86_64         2.0.9-7.el7            os                                                   29 k

Transaction Summary
=====================================================================================================================================
Install  3 Packages (+3 Dependent packages)

Total size: 774 M
Total download size: 29 M
Downloading packages:
warning: /var/cache/yum/x86_64/7/mysql57-community/packages/mysql-community-common-5.7.26-1.el7.x86_64.rpm: Header V3 DSA/SHA1 Signature, key ID 5072e1f5: NOKEY
Public key for mysql-community-common-5.7.26-1.el7.x86_64.rpm is not installed
(1/5): mysql-community-common-5.7.26-1.el7.x86_64.rpm                                                         | 274 kB  00:00:03     
(2/5): mysql-community-client-5.7.27-1.el7.x86_64.rpm                                                         |  24 MB  00:00:04     
(3/5): numactl-libs-2.0.9-7.el7.x86_64.rpm                                                                    |  29 kB  00:00:00     
(4/5): mysql-community-libs-compat-5.7.27-1.el7.x86_64.rpm                                                    | 2.0 MB  00:00:00     
(5/5): mysql-community-libs-5.7.27-1.el7.x86_64.rpm                                                           | 2.2 MB  00:00:04     
-------------------------------------------------------------------------------------------------------------------------------------
Total                                                                                                3.6 MB/s |  29 MB  00:00:08     
Retrieving key from file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql
Importing GPG key 0x5072E1F5:
 Userid     : "MySQL Release Engineering <mysql-build@oss.oracle.com>"
 Fingerprint: a4a9 4068 76fc bd3c 4567 70c8 8c71 8d3b 5072 e1f5
 Package    : mysql80-community-release-el7-3.noarch (installed)
 From       : /etc/pki/rpm-gpg/RPM-GPG-KEY-mysql
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
Warning: RPMDB altered outside of yum.
  Installing : mysql-community-common-5.7.26-1.el7.x86_64                                                                        1/7 
  Installing : mysql-community-libs-5.7.27-1.el7.x86_64                                                                          2/7 
  Installing : mysql-community-client-5.7.27-1.el7.x86_64                                                                        3/7 
  Installing : numactl-libs-2.0.9-7.el7.x86_64                                                                                   4/7 
  Installing : mysql-community-server-5.7.26-1.el7.x86_64                                                                        5/7 
  Installing : mysql-community-libs-compat-5.7.27-1.el7.x86_64                                                                   6/7 
  Erasing    : 1:mariadb-libs-5.5.60-1.el7_5.x86_64                                                                              7/7 
  Verifying  : mysql-community-server-5.7.26-1.el7.x86_64                                                                        1/7 
  Verifying  : numactl-libs-2.0.9-7.el7.x86_64                                                                                   2/7 
  Verifying  : mysql-community-libs-compat-5.7.27-1.el7.x86_64                                                                   3/7 
  Verifying  : mysql-community-client-5.7.27-1.el7.x86_64                                                                        4/7 
  Verifying  : mysql-community-common-5.7.26-1.el7.x86_64                                                                        5/7 
  Verifying  : mysql-community-libs-5.7.27-1.el7.x86_64                                                                          6/7 
  Verifying  : 1:mariadb-libs-5.5.60-1.el7_5.x86_64

Installed:
  mysql-community-libs.x86_64 0:5.7.27-1.el7                     mysql-community-libs-compat.x86_64 0:5.7.27-1.el7                  
  mysql-community-server.x86_64 0:5.7.26-1.el7                  

Dependency Installed:
  mysql-community-client.x86_64 0:5.7.27-1.el7   mysql-community-common.x86_64 0:5.7.26-1.el7   numactl-libs.x86_64 0:2.0.9-7.el7  

Replaced:
  mariadb-libs.x86_64 1:5.5.60-1.el7_5                                                                                               

Complete!
```

