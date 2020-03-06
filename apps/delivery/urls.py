# _*_ coding:utf-8 _*_
# Author: zizle
from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'variety-info/', views.VarietyInformationView.as_view()),  # 品种基本信息上传的模型
    path(r'questions/', views.QuestionsListView.as_view()),
    path(r'answer/', views.CreateAnswerView.as_view()),
    path(r'storehouses/', views.StorehouseView.as_view()),
    re_path(r'storehouse/(?P<province>[\u4e00-\u9fa5]+)/', views.ProvinceStorehouseView.as_view()),  # 某省份下的仓库
    re_path(r'storehouse/(?P<variety>[a-z]{1,2})/', views.VarietyStorehouseView.as_view()),  # 品种下的仓库
    re_path(r'storehouse/(?P<sid>\d+)/', views.OneStorehouseView.as_view()),
]