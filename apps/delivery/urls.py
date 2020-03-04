# _*_ coding:utf-8 _*_
# Author: zizle
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('questions/', views.QuestionsListView.as_view()),

]