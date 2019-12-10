# _*_ coding:utf-8 _*_
# __Author__： zizle
from rest_framework import serializers
from .models import Module

# 主模块序列化器
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'name', 'is_active')