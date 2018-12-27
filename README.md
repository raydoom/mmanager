# mmanager

通过ssh方式连接docker和supervisor服务器，集中化管理不同主机上的容器和由supervisor管理的进程，并提供web端实时查看相应容器和进程的控制台日志的功能

#### 目前提供的功能

- 查看主机上的容器和进程状态
- 启动，停止，重启容器和supervisor管理的进程
- 实时查看容器和进程的控制台端日志

#### 所需组件

- python 3.6
- django 2.1.3（python模块）
- docker 3.5.1（python模块）
- paramiko 2.4.2（python模块）
- dwebsocket 0.5.10（python模块）
- pymysql 0.9.2（python模块）
- python-jenkins（python模块）
- bootstrap 3.3.6
- jquery 1.9.1
- fontawesome 4.7.0

#### TODO

- 为容器创建webshell，使用户能从web端连接到容器的shell，执行命令
