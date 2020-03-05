# _*_ coding:utf-8 _*_
# Author: zizle
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('questions/', views.QuestionsListView.as_view()),
    path('answer/', views.CreateAnswerView.as_view()),
    path('storehouses/', views.StorehouseView.as_view()),
]