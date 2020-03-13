# _*_ coding:utf-8 _*_
# Author: zizle


from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'
    verbose_name = "用户信息"
    # main_menu_index = 0  # admin后台的app排列顺序
