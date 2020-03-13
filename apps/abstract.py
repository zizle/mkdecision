# _*_ coding:utf-8 _*_
# __Author__： zizle
from django.db import models


# 模型基类
class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="加入时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True
