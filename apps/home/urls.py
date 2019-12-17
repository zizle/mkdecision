# _*_ coding:utf-8 _*_
# Author: zizle

from django.urls import path, re_path
from . import views

urlpatterns = [
    path('news/', views.NewsBulletinView.as_view()),  # 新闻公告视图
    re_path(r'^news/(?P<nid>\d+)/$', views.NewsBulletinRetrieveView.as_view()),  # 单个新闻公告详情视图
    path('advertise/', views.AdvertiseView.as_view()),  # 广告视图
    re_path(r'^advertise/(?P<aid>\d+)/$', views.AdvertiseRetrieveView.as_view()),  # 单个广告视图
    re_path(r'^advertise/(?P<name>[a-zA-Z0-9.]+)/$', views.AdvertiseWithNameView.as_view()),  # 单个广告视图
    re_path(r'^data-category/(?P<group>[a-z_]+)/$', views.DataCategoryView.as_view()),  # 某个组下的视图(不指定组)
    path(r'normal-report/', views.NormalReportView.as_view()),  # 常规报告视图
    re_path(r'^normal-report/(?P<rid>\d+)/$', views.NormalReportRetrieveView.as_view()),  # 单个常规报告视图
]
