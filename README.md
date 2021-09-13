# mmanager

通过ssh方式连接docker和supervisor服务器，集中化管理不同主机上的容器和由supervisor管理的进程，并提供web端实时查看相应容器和进程的控制台日志的功能

#### 主要功能

- 查看主机上的容器和进程状态
- 启动，停止，重启容器和supervisor管理的进程
- 实时查看容器和进程的控制台日志
- 容器webshell支持，功能与`docker exec -it xxxx bash`一致

#### 所需组件

- python 3
- django
- bootstrap 3.3.6
- jquery 1.9.1
- fontawesome 4.7.0

#### 使用方式

克隆代码到本地
```
git clone https://github.com/raydoom/mmanager.git
```
安装mysql数据库，新建mmanager数据库，导入mmanager.sql，修改config/config.ini中数据库相关的配置
```
CREATE DATABASE mmanager DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
use mmanager;
source mmanager.sql;
```
使用pip安装所需模块
```
pip3 install -r requirements.txt
```
开发调试
```
python3 manage.py runserver 0.0.0.0:8000
```

使用supervisor进行部署，配置示例（修改directory为项目所在目录）
```
[program:mmanager]
command=python3 manage.py runserver 0.0.0.0:8000                  
autostart=true
autorestart=unexpected
startsecs=1                                                      
directory=/opt/apppython/mmanager
stdout_logfile=/var/log/mmanager.log
redirect_stderr=true
stdout_logfile_maxbytes=10MB
stdout_logfile_backups=10
```
推荐使用supervisor或nohup进行部署，不推荐使用&放到后台运行，会导致websocket连接无法释放，进而导致系统资源浪费。
```
nohup python3 manage.py runserver 0.0.0.0:8000 >> /var/log/mmanager.log &
```

部署完成后，访问8000端口，默认用户admin/111111

#### docker部署
docker启动
```
docker run --name=mmanager -p 8000:8000 -e db_host=172.16.0.26 -e db_port=3306 -e db_use=root -e db_password=111111 raydoom/mmanager:latest
```
