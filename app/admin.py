# coding=utf8

from django.contrib import admin
from .models.jenkins_server_models import Jenkins_Server
from app.account.models import UserInfo
from app.server.models import Server, ServerType
# Register your models here.


admin.site.register(Jenkins_Server)
admin.site.register(UserInfo)
admin.site.register(Server)
admin.site.register(ServerType)
## 管理员 root   111111