# coding=utf8

from django.contrib import admin
from app.jenkins.models import JenkinsServer
from app.account.models import UserInfo
from app.server.models import Server, ServerType
# Register your models here.


admin.site.register(JenkinsServer)
admin.site.register(UserInfo)
admin.site.register(Server)
admin.site.register(ServerType)
## 管理员 root   111111