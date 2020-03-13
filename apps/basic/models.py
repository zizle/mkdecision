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


# 记录客户端打开的情况
class ClientOpenRecord(BaseModel):
    client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name='客户端')

    class Meta:
        db_table = 'basic_client_opened'
        verbose_name = '客户端打开记录'
        verbose_name_plural = verbose_name


""" 系统主功能模块相关 """


# 系统主功能模块以及子功能模块
class Module(BaseModel):
    name = models.CharField(max_length=16, unique=True, verbose_name="名称")
    parent = models.ForeignKey('self', related_name='sub_modules', null=True, blank=True, default=None, on_delete=models.CASCADE, verbose_name='父级')
    order = models.IntegerField(default=0, verbose_name="排序")
    is_active = models.BooleanField(default=True, verbose_name="启用")

    class Meta:
        db_table = "basic_module"
        verbose_name = "主功能菜单"
        verbose_name_plural = verbose_name


# 记录用户-客户端访问模块
class ModuleOpenRecord(BaseModel):
    client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name='客户端')
    module = models.ForeignKey('Module', on_delete=models.CASCADE, verbose_name='模块')
    user = models.ForeignKey('user.User', null=True, blank=True, on_delete=models.CASCADE, verbose_name='用户')

    class Meta:
        db_table = 'basic_module_opened'
        verbose_name = '模块访问记录'
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
    EXCHANGES = (
        (1, '郑州商品交易所'),
        (2, '上海期货交易所'),
        (3, '大连商品交易所'),
        (4, '中国金融期货交易所'),
        (5, '上海国际能源交易中心'),
    )
    group = models.ForeignKey('VarietyGroup', related_name='varieties', on_delete=models.CASCADE, verbose_name='所属组')
    name = models.CharField(max_length=16, verbose_name='名称')
    name_en = models.CharField(max_length=32, verbose_name='名称')
    exchange = models.SmallIntegerField(choices=EXCHANGES, default=0, verbose_name='交易所')
    is_active = models.BooleanField(default=True, verbose_name='有效')

    class Meta:
        db_table = 'basic_variety'
        verbose_name = '品种'
        verbose_name_plural = verbose_name
        unique_together = (('group', 'name'), ('group', 'name_en'),)
