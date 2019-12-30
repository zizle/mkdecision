# _*_ coding:utf-8 _*_
# __Author__： zizle
from django.db import models
from apps.abstract import BaseModel


# 短信通
class MessageLink(BaseModel):
    date = models.DateField(verbose_name='日期')
    time = models.TimeField(verbose_name='时间')
    content = models.CharField(max_length=2048, verbose_name='内容')
    creator = models.ForeignKey('user.User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者')

    class Meta:
        db_table = 'info_message_link'
        verbose_name = '短信通'
        verbose_name_plural = verbose_name


# 市场分析
class MarketAnalysis(BaseModel):
    name = models.CharField(max_length=256, verbose_name='名称')
    file = models.FileField(upload_to='info/marketAly/%Y/%m/%d/')
    creator = models.ForeignKey('user.User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者')

    class Meta:
        db_table = 'info_market_analysis'
        verbose_name = '市场分析'
        verbose_name_plural = verbose_name

