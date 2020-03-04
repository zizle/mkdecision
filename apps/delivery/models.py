# _*_ coding:utf-8 _*_
# Author: zizle
from django.db import models
from apps.abstract import BaseModel
from basic.models import Variety


# 交易所的服务指引
class ServiceGuide(BaseModel):

    name = models.CharField(max_length=32, verbose_name='名称')
    en_code = models.CharField(max_length=32, verbose_name='英文代称')
    exchange = models.SmallIntegerField(choices=Variety.EXCHANGES, default=0, verbose_name='从属于')

    class Meta:
        db_table = 'delivery_service_guide'
        verbose_name = '服务指引'
        verbose_name_plural = '服务指引'


""" 交流与讨论 """


class Question(BaseModel):
    STATUS = (
        (0, '审核中'),
        (1, '已通过'),
    )
    content = models.CharField(max_length=512, verbose_name='内容')
    questioner = models.ForeignKey('user.User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='提问人')
    read_count = models.IntegerField(default=0, verbose_name='阅读量')
    status = models.IntegerField(choices=STATUS, default=0, verbose_name='状态')

    class Meta:
        db_table = 'delivery_question'
        verbose_name = '问题'
        verbose_name_plural = '问题'


class Answer(BaseModel):
    STATUS = (
        (0, '审核中'),
        (1, '已通过'),
    )
    content = models.CharField(max_length=512, verbose_name='内容')
    answerer = models.ForeignKey('user.User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='回答者')
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='问题')
    attach_to = models.ForeignKey('Answer', blank=True, null=True, on_delete=models.CASCADE, verbose_name='从属于')
    status = models.IntegerField(choices=STATUS, default=0, verbose_name='状态')

    class Meta:
        db_table = 'delivery_answer'
        verbose_name = '答案'
        verbose_name_plural = '答案'

