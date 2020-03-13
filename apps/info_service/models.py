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


# 调研报告
class SearchReport(BaseModel):
    name = models.CharField(max_length=256, verbose_name='名称')
    file = models.FileField(upload_to='info/searchRpt/%Y/%m/%d/')
    creator = models.ForeignKey('user.User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者')

    class Meta:
        db_table = 'info_search_report'
        verbose_name = '调研报告'
        verbose_name_plural = verbose_name


# 专题研究
class TopicSearch(BaseModel):
    name = models.CharField(max_length=256, verbose_name='名称')
    file = models.FileField(upload_to='info/topicSch/%Y/%m/%d/')
    creator = models.ForeignKey('user.User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者')

    class Meta:
        db_table = 'info_topic_search'
        verbose_name = '调研报告'
        verbose_name_plural = verbose_name


# 交易策略
class TradePolicy(BaseModel):
    date = models.DateField(verbose_name='日期')
    time = models.TimeField(verbose_name='时间')
    content = models.CharField(max_length=2048, verbose_name='内容')
    creator = models.ForeignKey('user.User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者')

    class Meta:
        db_table = 'info_trade_policy'
        verbose_name = '交易策略'
        verbose_name_plural = verbose_name


# 投资方案
class InvestPlan(BaseModel):
    name = models.CharField(max_length=256, verbose_name='名称')
    file = models.FileField(upload_to='info/ivtPlan/%Y/%m/%d/')
    creator = models.ForeignKey('user.User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者')

    class Meta:
        db_table = 'info_invest_plan'
        verbose_name = '投资方案'
        verbose_name_plural = verbose_name


# 套保方案
class HedgePlan(BaseModel):
    name = models.CharField(max_length=256, verbose_name='名称')
    file = models.FileField(upload_to='info/hedgePlan/%Y/%m/%d/')
    creator = models.ForeignKey('user.User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者')

    class Meta:
        db_table = 'info_hedge_plan'
        verbose_name = '套保方案'
        verbose_name_plural = verbose_name
