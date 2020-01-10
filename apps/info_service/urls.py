# _*_ coding:utf-8 _*_
# Author: zizle

from django.urls import path, re_path
from . import views

urlpatterns = [
    path('sms/', views.SMSLinkView.as_view()),  # 短信通
    re_path(r'^sms/(?P<mid>\d+)/$', views.SMSLinkRetrieveView.as_view()),  # 单个短信通
    path('market-analysis/', views.MarketAnalysisView.as_view()),  # 市场分析
    re_path(r'^market-analysis/(?P<mid>\d+)/$', views.MarketAnalysisRetrieveView.as_view()),  # 单个市场分析
    path('search-report/', views.SearchReportView.as_view()),  # 调研报告
    re_path(r'^search-report/(?P<sid>\d+)/$', views.SearchReportRetrieveView.as_view()),  # 单个调研报告
    path('topic-search/', views.TopicSearchView.as_view()),  # 专题研究
    re_path(r'^topic-search/(?P<sid>\d+)/$', views.TopicSearchRetrieveView.as_view()),  # 单个专题研究
    path('person-train/', views.PersonTrainView.as_view()),  # 顾问服务-人才培养
    path('dept-build/', views.DeptBuildView.as_view()),  # 顾问服务-部门组建
    path('inst-examine/', views.InstExamineView.as_view()),  # 顾问服务-制度考核
    path('trade-policy/', views.TradePolicyView.as_view()),  # 策略服务-交易策略
    re_path(r'^trade-policy/(?P<pid>\d+)/$', views.TradePolicyRetrieveView.as_view()),  # 单个交易策略
    path('invest-plan/', views.InvestPlanView.as_view()),  # 策略服务-投资方案
    re_path(r'^invest-plan/(?P<pid>\d+)/$', views.InvestPlanRetrieveView.as_view()),  # 单个投资方案
    path('hedge-plan/', views.HedgePlanView.as_view()),  # 策略服务-套保方案
    re_path(r'^hedge-plan/(?P<pid>\d+)/$', views.HedgePlanRetrieveView.as_view()),  # 单个套保方案

]
