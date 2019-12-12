# _*_ coding:utf-8 _*_
# __Author__： zizle
from django.db import models
from apps.abstract import BaseModel

""" 客户端相关 """


# 客户端模型
class Client(BaseModel):
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name="名称备注")
    machine_code = models.CharField(max_length=32, unique=True, verbose_name="机器识别码")
    is_manager = models.BooleanField(default=False, verbose_name="管理端")
    is_active = models.BooleanField(default=True, verbose_name="有效")

    class Meta:
        db_table = "basic_client"
        verbose_name = "客户端"
        verbose_name_plural = verbose_name


""" 系统主功能模块相关 """


# 系统主功能模块
class Module(BaseModel):
    name = models.CharField(max_length=16, unique=True, verbose_name="名称")
    order = models.IntegerField(default=0, verbose_name="排序")
    is_active = models.BooleanField(default=True, verbose_name="启用")

    class Meta:
        db_table = "basic_module"
        verbose_name = "主功能菜单"
        verbose_name_plural = verbose_name


""" 品种相关 """


# 品种的分组
class VarietyGroup(BaseModel):
    name = models.CharField(max_length=16, unique=True, verbose_name="组名")

    class Meta:
        db_table = 'basic_variety_group'
        verbose_name = "品种组别"
        verbose_name_plural = verbose_name


# 品种模型
class Variety(BaseModel):
    group = models.ForeignKey('VarietyGroup', related_name='varieties', on_delete=models.CASCADE, verbose_name='所属组')
    name = models.CharField(max_length=16, verbose_name='名称')
    name_en = models.CharField(max_length=32, verbose_name='名称')

    class Meta:
        db_table = 'basic_variety'
        verbose_name = '品种'
        verbose_name_plural = verbose_name
        unique_together = (('group', 'name'), ('group', 'name_en'),)
