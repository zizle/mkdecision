# _*_ coding:utf-8 _*_
# __Author__： zizle
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^access-module/(\-[129]|\d+)/$', views.ModuleAccessedView.as_view()),  # 用户模块权限
]
