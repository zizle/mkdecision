# _*_ coding:utf-8 _*_
# Author: zizle

from django.urls import path, re_path
from . import views

urlpatterns = [
    path('sms/', views.SMSLinkView.as_view()),   # 短信通
    re_path('^sms/(?P<mid>\d+)/$', views.SMSLinkRetrieveView.as_view()),   # 单个短信通
    path('market-analysis/', views.MarketAnalysisView.as_view()),  # 市场分析
    re_path('^market-analysis/(?P<mid>\d+)/$', views.MarketAnalysisRetrieveView.as_view()),   # 单个市场分析
]
