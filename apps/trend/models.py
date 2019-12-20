# _*_ coding:utf-8 _*_
# __Author__： zizle
from django.db import models
from apps.abstract import BaseModel


# 数据表的分组
class TrendTableGroup(BaseModel):
    name = models.CharField(max_length=16, unique=True, verbose_name="组名")
    variety = models.ForeignKey('basic.Variety', related_name='trend_table_groups', on_delete=models.CASCADE, verbose_name='所属品种')

    class Meta:
        db_table = 'trend_table_group'
        verbose_name = "数据表组别"
        verbose_name_plural = verbose_name
        unique_together = (('name', 'variety'),)


# 数据表
class TrendTable(BaseModel):
    name = models.CharField(max_length=256, verbose_name='名称')
    group = models.ForeignKey('TrendTableGroup', related_name='tables', on_delete=models.CASCADE, verbose_name='所属组别')
    sql_name = models.CharField(max_length=32, verbose_name='数据库中表名称')
    creator = models.ForeignKey('user.User', related_name='create_trend_tables', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者')
    editor = models.ForeignKey('user.User', related_name='edit_trend_tables', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='更新者')
    is_delete = models.BooleanField(default=False, verbose_name='已删除')

    class Meta:
        db_table = 'trend_table'
        verbose_name = "数据表名"
        verbose_name_plural = verbose_name
        unique_together = (('name', 'group'),)
