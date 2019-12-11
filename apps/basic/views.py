# _*_ coding:utf-8 _*_
# __Author__： zizle
import json
from django.views.generic import View
from django.http.response import HttpResponse
from utils.client import get_client
from .models import Client, Module
from .serializers import ClientSerializer, ModuleSerializer

""" 客户端相关 """


# 客户端视图
class ClientView(View):
    def get(self, request):
        machine_code = request.GET.get('mc', '')
        client = get_client(machine_code)
        user = request.user
        if not user or not client or not user.is_operator or not client.is_manager:
            all_clients = Client.objects.none()
        else:
            body_data = json.loads(request.body)
            # all_users = Client.objects.filter(**body_data).exclude(is_superuser=True)  # 根据需求获取用户(去除超级管理员)
            all_clients = Client.objects.filter(**body_data)  # 根据需求获取客户端(去除超级管理端)
        serializer = ClientSerializer(instance=all_clients, many=True)
        return HttpResponse(
            content=json.dumps({"message": '获取客户端列表成功!', "error": False, "data": serializer.data}),
            content_type="application/json; charset=utf-8",
            status=200
        )

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


# 单个客户端视图
class ClientRetrieveView(View):
    def get(self, request, cid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        try:
            if not client:
                raise ValueError('INVALID CLIENT.')
            operate_client = Client.objects.get(id=int(cid))
        except Client.DoesNotExist:
            data = {}
            message = '该客户端不存在.'
            status_code = 400
        except Exception as e:
            data = {}
            message = str(e)
            status_code = 400
        else:
            message = '获取客户端信息成功！'
            data = {
                'name': operate_client.name if operate_client.name else '',
                'machine_code': operate_client.machine_code
            }
            status_code = 200
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

    # 修改部分信息
    def patch(self, request, cid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT.')
            if not request_user or not request_user.is_operator:
                raise ValueError('登录已过期或不能进行这个操作!')
            new_data = json.loads(request.body)
            operate_client = Client.objects.get(id=int(cid))
            for key, value in new_data.items():
                if key in ['name', 'machine_code', 'is_active']:
                    operate_client.__setattr__(key, value)
            operate_client.save()
            message = '修改成功!'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": {}}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


""" 系统模块相关 """


# 系统模块视图
class ModuleView(View):
    def get(self, request):
        machine_code = request.GET.get('mc', '')
        client = get_client(machine_code)
        if not client:
            all_modules = Module.objects.none()
        else:
            all_modules = Module.objects.all().order_by('order')  # 获取系统模块
        serializer = ModuleSerializer(instance=all_modules, many=True)
        return HttpResponse(
            content=json.dumps({"message": '获取模块列表成功!', "data": serializer.data}),
            content_type="application/json; charset=utf-8",
            status=200
        )

    def post(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_operator:
                raise ValueError('还没登录或不能进行这个操作!')
            body_data = json.loads(request.body)
            name = body_data.get('name', None)
            if not name:
                raise ValueError('请输入正确的名称.')
            # 创建
            module = Module(name=name)
            module.save()
            data = {'id': module.id, 'name': module.name}
            message = '创建新模块成功!'
            status_code = 201
        except Exception as e:
            message = str(e)
            status_code = 400
            data = {}
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


# 单个模块基础信息视图
class ModuleRetrieveView(View):
    def get(self, request, mid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        try:
            if not client:
                raise ValueError('INVALID CLIENT.')
            operate_module = Module.objects.get(id=int(mid))
        except Module.DoesNotExist:
            data = {}
            message = '该模块不存在.'
            status_code = 400
        except Exception as e:
            data = {}
            message = str(e)
            status_code = 400
        else:
            message = '获取模块信息成功！'
            data = {'name': operate_module.name}
            status_code = 200
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

    # 修改部分信息
    def patch(self, request, mid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT.')
            if not request_user or not request_user.is_operator:
                raise ValueError('登录已过期或不能进行这个操作!')
            new_data = json.loads(request.body)
            operate_module = Module.objects.get(id=int(mid))
            for key, value in new_data.items():
                if key in ['name', 'is_active']:
                    operate_module.__setattr__(key, value)
            operate_module.save()
            message = '修改成功!'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": {}}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )
