# _*_ coding:utf-8 _*_
# Author: zizle
from django.db import models
from apps.abstract import BaseModel
from basic.models import Variety

""" 品种的基本信息 """


# 品种基本信息模型
class VarietyInformation(BaseModel):
    variety = models.ForeignKey('basic.Variety', related_name='infos', on_delete=models.CASCADE, verbose_name="品种")
    delivery_date = models.CharField(max_length=64, null=True, blank=True, verbose_name='最后交易日')
    warrant_expire_date = models.CharField(max_length=512, null=True, blank=True, verbose_name='仓单有效期')
    delivery_unit_min = models.CharField(max_length=64, null=True, blank=True, verbose_name='最小交割单位')

    class Meta:
        db_table = 'delivery_variety_info'
        verbose_name = '品种基本信息'
        verbose_name_plural = '品种基本信息'



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


""" 仓库数据 """


# 交割仓库信息(与品种多对多)
class StoreHouse(BaseModel):
    variety = models.ManyToManyField('basic.Variety', verbose_name='品种')
    province = models.CharField(max_length=16, verbose_name='所属省份')
    name = models.CharField(max_length=64, verbose_name='名称')
    house_code = models.CharField(max_length=8, unique=True, verbose_name='仓库编码')
    arrived = models.CharField(max_length=512, verbose_name='到达站')
    premium = models.CharField(max_length=512, verbose_name='升贴水')
    address = models.CharField(max_length=512, verbose_name='地址')
    link = models.CharField(max_length=256, verbose_name='联系人')
    tel_phone = models.CharField(max_length=512, verbose_name='联系电话')
    fax = models.CharField(max_length=64, verbose_name='传真')
    longitude = models.FloatField(verbose_name='经度')
    latitude = models.FloatField(verbose_name='纬度')

    class Meta:
        db_table = 'delivery_storehouse'
        verbose_name = '交割仓库'
        verbose_name_plural = '交割仓库'

