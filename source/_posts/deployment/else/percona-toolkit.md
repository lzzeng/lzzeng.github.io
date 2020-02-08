---
title: Percona toolkit
date: 2019-10-14 14:51:24
tags:
    - MySQL
categories:
    - 其它
toc: true
---



## **安装**

```sh
wget https://www.percona.com/downloads/percona-toolkit/2.2.7/RPM/percona-toolkit-2.2.7-1.noarch.rpm
yum install percona-toolkit-2.2.7-1.noarch.rpm -y
yum install perl-Digest-MD5 -y
```

<!-- more -->

```sh
Installed:
  percona-toolkit.noarch 0:2.2.7-1                                                                                                   

Dependency Installed:
  perl.x86_64 4:5.16.3-294.el7_6                perl-Carp.noarch 0:1.26-244.el7         perl-Compress-Raw-Bzip2.x86_64 0:2.061-3.el7 
  perl-Compress-Raw-Zlib.x86_64 1:2.061-4.el7   perl-DBD-MySQL.x86_64 0:4.023-6.el7     perl-DBI.x86_64 0:1.627-4.el7                
  perl-Data-Dumper.x86_64 0:2.145-3.el7         perl-Encode.x86_64 0:2.51-7.el7         perl-Exporter.noarch 0:5.68-3.el7            
  perl-File-Path.noarch 0:2.09-2.el7            perl-File-Temp.noarch 0:0.23.01-3.el7   perl-Filter.x86_64 0:1.49-3.el7              
  perl-Getopt-Long.noarch 0:2.40-3.el7          perl-HTTP-Tiny.noarch 0:0.033-3.el7     perl-IO-Compress.noarch 0:2.061-2.el7        
  perl-IO-Socket-IP.noarch 0:0.21-5.el7         perl-IO-Socket-SSL.noarch 0:1.94-7.el7  perl-Mozilla-CA.noarch 0:20130114-5.el7      
  perl-Net-Daemon.noarch 0:0.48-5.el7           perl-Net-LibIDN.x86_64 0:0.12-15.el7    perl-Net-SSLeay.x86_64 0:1.55-6.el7          
  perl-PathTools.x86_64 0:3.40-5.el7            perl-PlRPC.noarch 0:0.2020-14.el7       perl-Pod-Escapes.noarch 1:1.04-294.el7_6     
  perl-Pod-Perldoc.noarch 0:3.20-4.el7          perl-Pod-Simple.noarch 1:3.28-4.el7     perl-Pod-Usage.noarch 0:1.63-3.el7           
  perl-Scalar-List-Utils.x86_64 0:1.27-248.el7  perl-Socket.x86_64 0:2.010-4.el7        perl-Storable.x86_64 0:2.45-3.el7            
  perl-Text-ParseWords.noarch 0:3.29-4.el7      perl-Time-HiRes.x86_64 4:1.9725-3.el7   perl-Time-Local.noarch 0:1.2300-2.el7        
  perl-constant.noarch 0:1.27-2.el7             perl-libs.x86_64 4:5.16.3-294.el7_6     perl-macros.x86_64 4:5.16.3-294.el7_6        
  perl-parent.noarch 1:0.225-244.el7            perl-podlators.noarch 0:2.5.1-3.el7     perl-threads.x86_64 0:1.87-4.el7             
  perl-threads-shared.x86_64 0:1.43-6.el7      

Complete!
```



## **权限**

```sh
GRANT ALL PRIVILEGES ON `zabbix`.* TO 'pt'@'%'

show grants for 'root'@'192.168.1.101';

revoke SELECT, INSERT, UPDATE, DELETE, CREATE, PROCESS, SUPER, REPLICATION SLAVE ON *.* FROM 'root'@'192.168.1.101';
```



## **执行**

pt-table-checksum

```sh
#pt-table-checksum --nocheck-replication-filters --no-check-binlog-format --replicate=test_sync.checksums --create-replicate-table --databases=test_sync --tables=contact h=10.1.7.211,u=root,p=mysqlxxx,P=3306

pt-table-checksum --nocheck-replication-filters --no-check-binlog-format --replicate=test_sync.checksums --create-replicate-table --databases=test_sync h=10.1.7.211,u=root,p=mysqlxxx,P=3306
```



pt-table-sync

```sh
#pt-table-sync --replicate=test_sync.checksums h=10.1.7.211,u=root,p=mysqlxxx,P=3306 h=10.1.7.211,u=root,p=mysqlxxx,P=3307 --print

pt-table-sync --replicate=test_sync.checksums h=10.1.7.211,u=root,p=mysqlxxx,P=3306 h=10.1.7.211,u=root,p=mysqlxxx,P=3307 --execute
```



err:

```sh
Can't make changes on the master because no unique index exists at /usr/bin/pt-table-sync line 10649.  while doing zabbix.history on 172.17.0.3
```



pt-heartbeat

```sh
#pt-heartbeat --user=root --ask-pass --host=10.1.7.211 --port 3306 --create-table -D test_sync --interval=1 --update --replace --daemonize

#pt-heartbeat -D test_sync --table=heartbeat --monitor --host=10.1.7.211 --port=3306 --user=root --password=mysqlxxx --master-server-id=100 --print-master-server-id

pt-heartbeat -D test_sync --table=heartbeat --check --host=10.1.7.211 --port=3306 --user=root --password=mysqlxxx --master-server-id=100 --print-master-server-id

#pt-heartbeat --stop
```








