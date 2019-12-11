# _*_ coding:utf-8 _*_
# __Author__： zizle
import datetime
from rest_framework import serializers
from basic.models import Client


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

