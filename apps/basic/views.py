# _*_ coding:utf-8 _*_
# __Author__： zizle
import json
from django.views.generic import View
from django.http.response import HttpResponse
from utils.client import get_client
from .models import Client


# 客户端视图
class ClientView(View):
    def post(self, request):
        try:
            body_data = json.loads(request.body)
            name = body_data.get('name', None)
            machine_code = body_data.get('machine_code', None)
            is_manager = body_data.get('is_manager', False)
            if not machine_code:
                raise ValueError('缺少【机器码】.')
            # 查询客户端存在与否
            client = get_client(machine_code)
            if client:  # 存在，更新身份
                client.is_manager = is_manager
            else:  # 不存在则创建
                client = Client(
                    name=name,
                    machine_code=machine_code,
                    is_manager=is_manager
                )
            client.save()
            message = '创建成功.'
            status_code = 200
            data = {'machine_code': client.machine_code}
        except Exception as e:
            message = str(e)
            status_code = 400
            data = {}
        return HttpResponse(
            content=json.dumps({'message': message, 'data': data}),
            content_type='application/json; charset=utf-8',
            status=status_code
        )
