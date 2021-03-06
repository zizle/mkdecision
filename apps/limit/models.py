# _*_ coding:utf-8 _*_
# __Author__： zizle
from django.db import models
from django.conf import settings
from apps.abstract import BaseModel


# 用户可登录的客户端关系表
class UserToClient(BaseModel):
    user = models.ForeignKey(to='user.User', on_delete=models.CASCADE, verbose_name="用户")
    client = models.ForeignKey(to='basic.Client', on_delete=models.CASCADE, verbose_name="客户端")
    expire_date = models.DateField(default=settings.DEFAULT_EXPIRE_DATE, verbose_name="失效时间")

    class Meta:
        db_table = "limit_user_client"
        verbose_name = '用户-客户端'
        verbose_name_plural = verbose_name
        unique_together = (('user', 'client'),)


# 用户可访问的模块关系表
class UserToModule(BaseModel):
    user = models.ForeignKey(to='user.User', on_delete=models.CASCADE, verbose_name="用户")
    module = models.ForeignKey(to='basic.Module', on_delete=models.CASCADE, verbose_name="模块")
    expire_date = models.DateField(default=settings.DEFAULT_EXPIRE_DATE, verbose_name="失效时间")

    class Meta:
        db_table = "limit_user_module"
        verbose_name = '用户-模块'
        verbose_name_plural = verbose_name
        unique_together = (('user', 'module'),)


# 用户拥有权限的品种关系表
class UserToVariety(BaseModel):
    user = models.ForeignKey(to='user.User', on_delete=models.CASCADE, verbose_name="用户")
    variety = models.ForeignKey(to='basic.Variety', on_delete=models.CASCADE, verbose_name="品种")
    expire_date = models.DateField(default=settings.DEFAULT_EXPIRE_DATE, verbose_name="失效时间")

    class Meta:
        db_table = "limit_user_variety"
        verbose_name = '用户-品种'
        verbose_name_plural = verbose_name
        unique_together = (('user', 'variety'),)