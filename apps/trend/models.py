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
    origin_note = models.CharField(max_length=512, null=True, blank=True, verbose_name='数据来源')
    is_deleted = models.BooleanField(default=False, verbose_name='已删除')

    class Meta:
        db_table = 'trend_table'
        verbose_name = "数据表名"
        verbose_name_plural = verbose_name
        unique_together = (('name', 'group'),)


# 品种数据图
class VarietyChart(BaseModel):
    CATEGORY = (
        ('line', '折线图'),
        ('bar', '柱形图'),
        ('double_line', '双轴折线图'),
        ('double_bar', '双轴柱形图'),
    )
    name = models.CharField(max_length=64, unique=True, verbose_name="图表名")
    category = models.CharField(max_length=32, choices=CATEGORY, verbose_name='图表类型')
    variety = models.ForeignKey('basic.Variety', related_name='charts', on_delete=models.CASCADE,
                                verbose_name='所属品种')
    table = models.ForeignKey('TrendTable', related_name='table_charts', on_delete=models.CASCADE,
                              verbose_name='数据表')
    x_bottom = models.CharField(max_length=16, verbose_name='x轴')
    x_top = models.CharField(max_length=16, null=True, blank=True, verbose_name='上x轴')
    y_left = models.CharField(max_length=32, verbose_name='左轴')
    y_right = models.CharField(max_length=32, null=True, blank=True, verbose_name='右轴')
    x_bottom_label = models.CharField(max_length=32, null=True, blank=True, verbose_name='x轴名称')
    x_top_label = models.CharField(max_length=32, null=True, blank=True, verbose_name='上x轴名称')
    y_left_label = models.CharField(max_length=32, null=True, blank=True, verbose_name='y轴名称')
    y_right_label = models.CharField(max_length=32, null=True, blank=True, verbose_name='右y轴名称')
    start = models.CharField(max_length=32, null=True, blank=True, verbose_name='起始')
    end = models.CharField(max_length=32, null=True, blank=True, verbose_name='终止')
    is_top = models.BooleanField(default=False, verbose_name='主页展示')
    is_show = models.BooleanField(default=False, verbose_name='品种展示')
    creator = models.ForeignKey('user.User', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='创建者')

    class Meta:
        db_table = 'trend_variety_chart'
        verbose_name = "品种图表"
        verbose_name_plural = verbose_name
        unique_together = (('name', 'variety'),)
