# _*_ coding:utf-8 _*_
# Author: zizle

from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^(?P<vid>\d+)/group-tables/$', views.GroupTablesView.as_view()),  # 获取数据的组别(以品种vid为条件)
    path(r'varieties/group/', views.VarietiesTrendGroupView.as_view()),  # 所有品种下的所有数据组
    re_path(r'^group/(?P<gid>\d+)/table/$', views.GroupRetrieveTablesView.as_view()),  # 单个数据组下的表格，新建数据表
    re_path(r'^table/(?P<tid>\d+)/$', views.RetrieveTableView.as_view()),  # 某个数据表的详情图
    path(r'chart/', views.ChartView.as_view()),  # 品种图表
    re_path(r'^(?P<vid>\d+)/chart/$', views.VarietyChartView.as_view()),  # 某品种下的所有图表
    re_path(r'^chart/(?P<cid>\d+)/$', views.ChartRetrieveView.as_view()),  # 单个图表视图
]
