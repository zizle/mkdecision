# _*_ coding:utf-8 _*_
# __Author__： zizle
from django.db import models
from apps.abstract import BaseModel


# 新闻公告
class NewsBulletin(BaseModel):
    title = models.CharField(max_length=64, verbose_name='标题')
    creator = models.ForeignKey('user.User', null=True, on_delete=models.SET_NULL, verbose_name='创建者')
    file = models.FileField(upload_to='home/news/%Y/%m/%d/', blank=True, verbose_name='文件')
    content = models.TextField(blank=True, verbose_name='内容')

    class Meta:
        db_table = 'home_news'
        verbose_name = '新闻公告'
        verbose_name_plural = verbose_name


# 广告轮播
class Advertisement(BaseModel):
    name = models.CharField(max_length=64, verbose_name='标题')
    creator = models.ForeignKey('user.User', null=True, on_delete=models.SET_NULL, verbose_name='创建者')
    image = models.FileField(upload_to='home/advertisement/image/', verbose_name='图片')
    file = models.FileField(upload_to='home/advertisement/', blank=True, verbose_name='文件')
    content = models.TextField(blank=True, verbose_name='内容')

    class Meta:
        db_table = 'home_advertisement'
        verbose_name = '首页广告'
        verbose_name_plural = verbose_name

