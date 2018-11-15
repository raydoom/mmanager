# mmanager

通过访问docker和supervisor的远程管理接口，集中化管理不同主机上的容器和由supervisor管理的进程，并提供web端实时查看相应容器和进程的控制台日志的功能

目前提供的功能

- 查看主机上的容器和进程状态
- 启动，停止，重启容器和supervisor管理的进程
- 实时查看容器和进程的控制台端日志

### 所需组件

- python3.6
- django2.1.3
- docker3.5.1
- mysqlclient
- bootstrap + jquery UI

### TODO

- 优化日志查看功能