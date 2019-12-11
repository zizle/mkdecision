# _*_ coding:utf-8 _*_
# __Author__： zizle
from rest_framework import serializers
from .models import Client, Module


# 客户端序列化器
class ClientSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ('id', 'name', 'machine_code', 'category', 'is_active')

    @staticmethod
    def get_category(obj):
        return '管理端' if obj.is_manager else '普通端'

    @staticmethod
    def get_is_active(obj):
        return 1 if obj.is_active else 0

    @staticmethod
    def get_name(obj):
        return obj.name if obj.name else ''


# 主模块序列化器
class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'name', 'is_active')

