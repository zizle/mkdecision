# _*_ coding:utf-8 _*_
# __Author__： zizle
import datetime
from rest_framework import serializers
from basic.models import Client, Module, Variety


# 用户客户端权限管理序列化器
class ClientsToUserSerializer(serializers.ModelSerializer):
    def __init__(self, accessed_clients, *args, **kwargs):
        super(ClientsToUserSerializer, self).__init__(*args, **kwargs)
        self.accessed_clients = accessed_clients
        self.accessed_clients_ids = [accessed.client.id for accessed in accessed_clients]

    accessed = serializers.SerializerMethodField()
    expire_date = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ('id', 'name', 'machine_code', 'accessed', 'expire_date', 'category')

    def get_accessed(self, obj):
        if obj.id in self.accessed_clients_ids:
            return 1
        else:
            return 0

    def get_expire_date(self, obj):
        expire_date = ''
        for user_to_client in self.accessed_clients:
            if user_to_client.client.id == obj.id:
                expire_date = datetime.datetime.strftime(user_to_client.expire_date, '%Y-%m-%d')
        return expire_date

    @staticmethod
    def get_name(obj):
        return obj.name if obj.name else ''

    def get_category(self, obj):
        return '管理端' if obj.is_manager else '普通端'


# 用户系统模块权限管理序列化器
class ModulesToUserSerializer(serializers.ModelSerializer):
    def __init__(self, accessed_modules, *args, **kwargs):
        super(ModulesToUserSerializer, self).__init__(*args, **kwargs)
        self.accessed_modules = accessed_modules
        self.accessed_modules_ids = [accessed.module.id for accessed in accessed_modules]

    accessed = serializers.SerializerMethodField()
    expire_date = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ('id', 'name', 'accessed', 'expire_date')

    def get_accessed(self, obj):
        if obj.id in self.accessed_modules_ids or obj.name == u'首页':
            return 1
        else:
            return 0

    def get_expire_date(self, obj):
        expire_date = '3000-01-01' if obj.name == u'首页' else ''
        for user_to_module in self.accessed_modules:
            if user_to_module.module.id == obj.id:
                expire_date = datetime.datetime.strftime(user_to_module.expire_date, '%Y-%m-%d')
        return expire_date


# 用户品种权限管理序列化器
class VarietiesToUserSerializer(serializers.ModelSerializer):
    def __init__(self, accessed_varieties, *args, **kwargs):
        super(VarietiesToUserSerializer, self).__init__(*args, **kwargs)
        self.accessed_varieties = accessed_varieties
        self.accessed_varieties_ids = [accessed.variety.id for accessed in accessed_varieties]

    group = serializers.SlugRelatedField(slug_field='name', read_only=True)
    accessed = serializers.SerializerMethodField()
    expire_date = serializers.SerializerMethodField()

    class Meta:
        model = Variety
        fields = ('id', 'name', 'name_en', 'group', 'accessed', 'expire_date')

    def get_accessed(self, obj):
        if obj.id in self.accessed_varieties_ids:
            return 1
        else:
            return 0

    def get_expire_date(self, obj):
        expire_date = ''
        for user_to_variety in self.accessed_varieties:
            if user_to_variety.variety.id == obj.id:
                expire_date = datetime.datetime.strftime(user_to_variety.expire_date, '%Y-%m-%d')
        return expire_date
