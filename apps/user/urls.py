# _*_ coding:utf-8 _*_
# Author: zizle

from django.urls import path, re_path
from . import views
from limit.views import UserToClientView

urlpatterns = [
    path(r'superuser/', views.SuperUserView.as_view()),  # 超级管理员视图
    path(r'login/', views.UserLoginView.as_view()),  # 用户登录
    path(r'keep-online/', views.UserKeepOnline.as_view()),  # 用户打开软件自动登录(状态保持)
    path(r'', views.UsersView.as_view()),  # 用户视图(根据过滤条件获取相应用户)
    path(r'register/', views.UserRegisterView.as_view()),  # 普通用户注册
    re_path(r'^(?P<uid>\d+)/baseInfo/$', views.UserBaseInfoView.as_view()),  # 用户基础信息视图
    re_path(r'^(?P<uid>\d+)/clients/$', UserToClientView.as_view()),  # 用户客户端权限视图(维护用户客户端权限)

]
