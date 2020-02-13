# _*_ coding:utf-8 _*_
# Author: zizle

from django.urls import path, re_path
from . import views
from limit.views import UserToClientView, UserToModuleView, UserToVarietyView

urlpatterns = [
    path(r'superuser/', views.SuperUserView.as_view()),  # 超级管理员视图
    path(r'login/', views.UserLoginView.as_view()),  # 用户登录
    path(r'keep-online/', views.UserKeepOnline.as_view()),  # 用户打开软件自动登录(状态保持)
    path(r'', views.UsersView.as_view()),  # 用户视图(根据过滤条件获取相应用户)、普通用户注册
    re_path(r'^(?P<uid>\d+)/baseInfo/$', views.UserBaseInfoView.as_view()),  # 用户基础信息视图
    re_path(r'^(?P<uid>\d+)/clients/$', UserToClientView.as_view()),  # 用户客户端权限视图(维护用户客户端权限)
    re_path(r'^(?P<uid>\d+)/modules/$', UserToModuleView.as_view()),  # 用户模块权限视图(维护用户模块权限)
    re_path(r'^(?P<uid>\d+)/varieties/$', UserToVarietyView.as_view()),  # 用户品种权限视图(维护用户模块权限)
    re_path(r'^(?P<uid>\d+)/avatar/$', views.UserAvatarView.as_view()),  # 用户头像修改
    re_path(r'^(?P<uid>\d+)/psd/$', views.UserPasswordView.as_view()),  # 用户密码修改
]
