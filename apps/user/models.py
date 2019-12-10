# _*_ coding:utf-8 _*_
# Author: zizle

import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# 用户模型管理器
class UserManager(BaseUserManager):
    def create_user(self, phone, email, password, **extra_fields):
        print(extra_fields)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_operator', False)
        extra_fields.setdefault('is_collector', False)
        print(extra_fields)
        if not phone:
            raise ValueError('The given phone must be set')
        return self._create_user(phone, email, password, **extra_fields)

    def create_superuser(self, phone, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_operator', True)
        extra_fields.setdefault('is_collector', True)
        return self._create_user(phone, email, password, **extra_fields)

    def _create_user(self, phone, email, password, **extra_fields):
        # 对手机号进行验证
        if not re.match(r'^[1]([3-9])[0-9]{9}$', phone):
            raise ValueError('手机号格式有误.')
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


# 用户模型，不继承权限(每个模型的权限由自己设置第三方表构成)
class User(AbstractBaseUser):
    username = models.CharField(max_length=20, blank=True, verbose_name='用户名/昵称')
    phone = models.CharField(max_length=11, unique=True, verbose_name='手机')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="加入时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    note = models.CharField(max_length=20, blank=True, null=True, verbose_name='备注')
    is_superuser = models.BooleanField(default=False, verbose_name='超级管理员')
    is_operator = models.BooleanField(default=False, verbose_name='运营管理员')
    is_collector = models.BooleanField(default=False, verbose_name='信息管理员')
    is_researcher = models.BooleanField(default=False, verbose_name='品种研究员')
    is_active = models.BooleanField(default=True, verbose_name='有效用户')

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'user_user'
        verbose_name = '用户'  # 可读的模型名称
        verbose_name_plural = '用户'  # 可读的模型名称复数形式

    def get_full_name(self):
        full_name = '%s %s' % (self.username, self.phone)
        return full_name.strip()

    def get_short_name(self):
        return self.username

