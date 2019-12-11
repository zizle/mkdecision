# _*_ coding:utf-8 _*_
# Author: zizle

from django.urls import path, re_path
from . import views

urlpatterns = [
    path('client/', views.ClientView.as_view()),  # 客户端视图
    re_path(r'^client/(?P<cid>\d+)/$', views.ClientRetrieveView.as_view()),  # 客户端基础信息视图
    path('module/', views.ModuleView.as_view()),  # 系统模块视图
    re_path(r'^module/(?P<mid>\d+)/$', views.ModuleRetrieveView.as_view()),  # 单个模块基础信息视图
]
