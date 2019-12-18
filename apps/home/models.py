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


# 常规报告、交易通知等数据菜单分类模型
class DataCategory(BaseModel):
    GROUPS = (
        ('normal_report', '常规报告'),
        ('transaction_notice', '交易通知'),
    )
    name = models.CharField(max_length=16, verbose_name='名称')
    group = models.CharField(max_length=32, choices=GROUPS, verbose_name='组别')

    class Meta:
        db_table = 'home_data_category'
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        unique_together = (('name', 'group'),)


# 常规报告模型
class NormalReport(BaseModel):
    name = models.CharField(max_length=256, verbose_name='文件名')
    file = models.FileField(upload_to='home/normalReport/%Y/%m/%d/')
    date = models.DateField(verbose_name='报告日期')
    uploader = models.ForeignKey('user.User', related_name='report_files', null=True, on_delete=models.SET_NULL,
                                 verbose_name='上传者')
    category = models.ForeignKey('DataCategory', related_name='normal_reports', null=True, on_delete=models.CASCADE,
                                 verbose_name='所属分类')
    varieties = models.ManyToManyField('basic.Variety', related_name='variety_reports', verbose_name='所属品种')

    class Meta:
        db_table = 'home_normal_report'
        verbose_name = '常规报告'
        verbose_name_plural = verbose_name
        unique_together = (('name', 'date'),)


# 交易通知模型
class TransactionNotice(BaseModel):
    name = models.CharField(max_length=256, verbose_name='文件名')
    file = models.FileField(upload_to='home/transactionNotice/%Y/%m/%d/')
    date = models.DateField(verbose_name='通知日期')
    uploader = models.ForeignKey('user.User', related_name='notice_files', null=True, on_delete=models.SET_NULL,
                                 verbose_name='上传者')
    category = models.ForeignKey('DataCategory', related_name='transaction_notice', null=True, on_delete=models.CASCADE,
                                 verbose_name='所属分类')

    class Meta:
        db_table = 'home_transaction_notice'
        verbose_name = '交易通知'
        verbose_name_plural = verbose_name
        unique_together = (('name', 'date'),)


# 现货报表模型
class SpotCommodity(BaseModel):
    name = models.CharField(max_length=64, verbose_name="名称")
    area = models.CharField(max_length=128, verbose_name="地区")
    level = models.CharField(max_length=16, verbose_name="等级")
    price = models.FloatField(verbose_name="价格")
    increase = models.FloatField(verbose_name='增减')
    date = models.DateField(verbose_name="日期")
    note = models.CharField(max_length=256, blank=True, null=True, verbose_name="备注")
    uploader = models.ForeignKey('user.User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='上传者')

    class Meta:
        db_table = "home_spot_commodity"
        unique_together = ('name', 'date')
        verbose_name = "现货报表"

