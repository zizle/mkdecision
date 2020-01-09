# _*_ coding:utf-8 _*_
# Author: zizle

from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^image_code/(?P<image_code_id>[\w-]+)/$', views.ImageCodeView.as_view()),
    path('client/', views.ClientView.as_view()),  # 客户端视图
    re_path(r'^client/(?P<cid>\d+)/$', views.ClientRetrieveView.as_view()),  # 客户端基础信息视图
    path('module/', views.ModuleView.as_view()),  # 系统模块视图(后台管理使用)
    path('module/start/', views.ModuleStartView.as_view()),  # 系统模块视图(开启时获取使用)
    re_path(r'^module/(?P<mid>\d+)/$', views.ModuleRetrieveView.as_view()),  # 单个模块基础信息视图
    path(r'group-varieties/', views.GroupVarietiesView.as_view()),  # 获取品种的组别(含组下品种)
    re_path(r'^group-varieties/(?P<gid>\d+)/$', views.GroupRetrieveVarietiesView.as_view()),  # 单个品种组下的所有品种
    re_path(r'variety/(?P<vid>\d+)/$', views.VarietyRetrieveView.as_view()),  # 某个品种详细视图
]
