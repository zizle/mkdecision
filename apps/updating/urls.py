# _*_ coding:utf-8 _*_
# Author: zizle
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.CheckVersionView.as_view()),  # 检查是否有新版本
    path('download/', views.DownLoadClientFile.as_view())  # 下载文件
]