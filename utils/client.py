# _*_ coding:utf-8 _*_
# __Author__： zizle
from basic.models import Client


# 获取客户端
def get_client(machine_code=None):
    try:
        client = Client.objects.get(machine_code=machine_code, is_active=True) if machine_code else None
    except Client.DoesNotExist:
        client = None
    return client
