# _*_ coding:utf-8 _*_
# __Author__： zizle
from rest_framework import serializers
from .models import User


# 用户模型序列化器
class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format('%Y-%m-%d %H:%M:%S'), read_only=True)
    role = serializers.SerializerMethodField()
    note = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'phone', 'email', 'role', 'last_login', 'role', 'note', 'is_active')

    @staticmethod
    def get_role(obj):
        if obj.is_superuser:
            return '超级管理员'
        elif obj.is_operator:
            return '运营管理员'
        elif obj.is_collector:
            return '信息管理员'
        elif obj.is_researcher:
            return '研究员'
        else:
            return '普通用户'

    @staticmethod
    def get_note(obj):
        return obj.note if obj.note else ''

    @staticmethod
    def get_is_active(obj):
        return 1 if obj.is_active else 0