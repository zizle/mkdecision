# _*_ coding:utf-8 _*_
# Author: zizle

from django.urls import path, re_path

from . import views

urlpatterns = [
    path('news/', views.NewsBulletinView.as_view()),  # 新闻公告视图
    re_path(r'^news/(?P<nid>\d+)/$', views.NewsBulletinRetrieveView.as_view()),  # 单个新闻公告详情视图
    path('advertise/', views.AdvertiseView.as_view()),  # 广告视图
    re_path(r'^advertise/(?P<aid>\d+)/$', views.AdvertiseRetrieveView.as_view()),  # 单个广告视图
    re_path(r'^advertise/(?P<name>[a-zA-Z0-9_.]+)/$', views.AdvertiseWithNameView.as_view()),  # 单个广告视图
    re_path(r'^data-category/(?P<group>[a-z_]+)/$', views.DataCategoryView.as_view()),  # 某个组下的视图(不指定组)
    path(r'normal-report/', views.NormalReportView.as_view()),  # 常规报告视图
    re_path(r'^normal-report/(?P<rid>\d+)/$', views.NormalReportRetrieveView.as_view()),  # 单个常规报告视图
    path(r'transaction_notice/', views.TransactionNoticeView.as_view()),  # 交易通知视图
    re_path(r'^transaction_notice/(?P<nid>\d+)/$', views.TransactionNoticeRetrieveView.as_view()),  # 单个交易通知视图
    path(r'spot-commodity/', views.SpotCommodityView.as_view()),  # 现货报表视图
    re_path(r'^spot-commodity/(?P<sid>\d+)/$', views.SpotCommodityRetrieveView.as_view()),  # 单条现货报表记录视图
    path(r'finance-calendar/', views.FinanceCalendarView.as_view()),  # 财经日历视图
    re_path(r'^finance-calendar/(?P<fid>\d+)/$', views.FinanceCalendarRetrieveView.as_view()),  # 财经日历视图
]
