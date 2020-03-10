# _*_ coding:utf-8 _*_
# __Author__： zizle
from rest_framework import serializers
from .models import Client, Module, VarietyGroup, Variety, ClientOpenRecord


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
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ('id', 'name', 'is_active')

    @staticmethod
    def get_is_active(obj):
        return 1 if obj.is_active else 0


""" 品种相关 """


# 品种序列化器
class VarietySerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Variety
        fields = ('id', 'name', 'name_en', 'group', 'exchange')


# 品种组序列化器
class VarietyGroupSerializer(serializers.ModelSerializer):
    varieties = VarietySerializer(many=True, read_only=True)

    class Meta:
        model = VarietyGroup
        fields = ('id', 'name', 'varieties')


# 客户端记录序列化器
class ClientOpenRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientOpenRecord
        fields = '__all__'

