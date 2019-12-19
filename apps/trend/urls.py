# _*_ coding:utf-8 _*_
# Author: zizle

from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^(?P<vid>\d+)/group-tables/$', views.GroupTablesView.as_view()),  # 获取数据的组别，含组下的表名称(以品种vid为条件)
    path(r'varieties/group/', views.VarietiesTrendGroupView.as_view()),  # 所有品种下的所有数据组
    re_path(r'^group/(?P<gid>\d+)/table/$', views.GroupRetrieveTablesView.as_view()),  # 单个数据组下的表格，新建数据表
]
