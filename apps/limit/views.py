# _*_ coding:utf-8 _*_
# __Author__： zizle
import json
import datetime
from django.views.generic import View
from django.http.response import HttpResponse
from basic.models import Client, Module, Variety
from utils.client import get_client
from .models import UserToModule, UserToClient, UserToVariety
from .serializers import ClientsToUserSerializer, ModulesToUserSerializer, VarietiesToUserSerializer
from user.models import User


# 系统模块权限视图
class ModuleAccessedView(View):
    def get(self, request, mid):
        machine_code = request.GET.get('mc', None)
        if not get_client(machine_code):
            return HttpResponse(
                content=json.dumps({"message": "INVALID CLIENT.", "data": {'permission': 0}}),
                content_type="application/json; charset=utf-8",
                status=200
            )
        user = request.user
        mid = int(mid)
        if mid < 0:  # 内部人员管理操作【数据管理】【运营管理】【权限管理】
            # 验证用户是否是内部人员
            if user and user.is_researcher:
                return HttpResponse(
                    content=json.dumps({"message": "通过", "data": {'permission': 1}}),
                    content_type="application/json; charset=utf-8",
                    status=200
                )
            else:
                HttpResponse(
                    content=json.dumps({"message": "'您还没登录或登录已过期\n请先登录再进行操作!", "data": {'permission': 0}}),
                    content_type="application/json; charset=utf-8",
                    status=200
                )
        # 其他普通模块的验证
        else:
            try:
                # 获取当前模块,先放行首页
                request_module = Module.objects.get(id=int(mid))
                if not request_module.name == u'首页':  # 不是首页模块才进行权限验证
                    if not user:
                        raise ValueError('您还没登录或登录已过期\n请先登录再进行操作!')
                    if not user.is_researcher:  # 非内部人员查询权限
                        # 查询用户可进入的当前模块（不存在则直接报错）
                        UserToModule.objects.get(
                            user_id=user.id,
                            module_id=int(mid),
                            expire_date__gt=datetime.date.today()
                        )
                # 是首页则直接由此放行了
                data = {'permission': 1}
                message = '通过'
            except UserToModule.DoesNotExist:
                message = '您还不能查看此功能,\n若已登录请联系管理员开放！'
                data = {'permission': 0}

            except Exception as e:
                message = str(e)
                data = {'permission': 0}

            return HttpResponse(
                content=json.dumps({"message": message, "data": data}),
                content_type="application/json; charset=utf-8",
                status=200
            )


# 用户客户端权限视图
class UserToClientView(View):
    # 获取所有客户端并标记当前用户可登录情况
    def get(self, request, uid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            body_data = json.loads(request.body)
            operate_user = User.objects.get(id=int(uid))
            # 当前用户可登录客户端
            accessed_clients = UserToClient.objects.filter(user=operate_user,
                                                           expire_date__gt=datetime.date.today())  # 第三关系表的实例
            # 所有有效的客户端
            all_clients = Client.objects.filter(**body_data)
            # 序列化
            serializer = ClientsToUserSerializer(accessed_clients=accessed_clients, instance=all_clients, many=True)
            message = '获取客户端信息成功!'
            status_code = 200
            data = serializer.data
        except Exception as e:
            message = str(e)
            status_code = 400
            data = []
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

    # 修改部分信息，可登录，有效期
    def patch(self, request, uid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_operator:
                raise ValueError('还没登录或不能进行这项操作!')
            # 获取可登录状态
            body_data = json.loads(request.body)
            client_id = body_data.get('client_id', None)
            if not client_id:
                raise ValueError('未指定的操作项目.')
            # 查询记录是否存在
            user_client = UserToClient.objects.filter(user_id=int(uid), client_id=int(client_id)).first()
            accessed = body_data.get('accessed', None)
            expire_date = body_data.get('expire_date', None)
            expire_date = datetime.datetime.strptime(expire_date, '%Y-%m-%d')
            if user_client and accessed:  # 存在，且设置为可登录,改变有效时间
                user_client.expire_date = expire_date
                user_client.save()
            elif user_client and not accessed:  # 存在，且设置为不可登录,改变有效时间为2000-01-01
                user_client.expire_date = datetime.datetime.strptime('2000-01-01', '%Y-%m-%d')
                user_client.save()
            elif not user_client and accessed:  # 不存在，且设置为可登录，创建数据库记录
                user_client = UserToClient(
                    user_id=int(uid),
                    client_id=int(client_id)
                )
                user_client.save()
            else:  # 不存在，且设置为不可登录(一般不存在这种情况), 直接忽略
                pass
            message = '设置成功！'
            status_code = 200
            data = {'expire_date': datetime.datetime.strftime(user_client.expire_date, '%Y-%m-%d')}
        except Exception as e:
            message = str(e)
            status_code = 400
            data = {'expire_date': ''}
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


# 用户系统模块权限视图
class UserToModuleView(View):
    # 获取所有模块并标记当前用户可进入情况
    def get(self, request, uid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            operate_user = User.objects.get(id=int(uid))
            print(operate_user)
            # 所有的模块
            all_modules = Module.objects.all()
            # 如果是内部人员，直接返回所有模块，并且是都可进入的
            if operate_user.is_researcher:
                data = list()
                for module in all_modules:
                    data.append({
                        'id': module.id,
                        'name': module.name,
                        'accessed': 1,
                        'expire_date': '3000-01-01'
                    })
            else:
                # 当前用户可进入的模块
                accessed_modules = UserToModule.objects.filter(user=operate_user,
                                                               expire_date__gt=datetime.date.today())  # 第三关系表的实例
                # 序列化
                serializer = ModulesToUserSerializer(accessed_modules=accessed_modules, instance=all_modules, many=True)
                data = serializer.data
            message = '获取模块信息成功!'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
            data = []
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

    # 修改部分信息，可登录，有效期
    def patch(self, request, uid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_operator:
                raise ValueError('还没登录或不能进行这项操作!')
            # 获取当前操作的用户
            operate_user = User.objects.get(id=int(uid))
            if operate_user.is_researcher:  # 用户是内部的人员不支持修改可进入或有效期状态
                raise ValueError('该人员不支持这项设置,请确认人员身份!')

            # 获取可登录状态
            body_data = json.loads(request.body)
            module_id = body_data.get('module_id', None)
            if not module_id:
                raise ValueError('未指定的操作项目.')
            # 获取当前修改的模块
            operate_module = Module.objects.get(id=int(module_id))
            if operate_module.name == u'首页':  # 首页模块是全开放的，不支持修改
                raise ValueError('【首页】不支持这项设置,请设置其他模块!')
            # 查询记录是否存在
            user_module = UserToModule.objects.filter(user_id=int(uid), module_id=int(module_id)).first()
            accessed = body_data.get('accessed', None)
            expire_date = body_data.get('expire_date', None)
            expire_date = datetime.datetime.strptime(expire_date, '%Y-%m-%d')
            if user_module and accessed:  # 存在，且设置为可登录,改变有效时间
                user_module.expire_date = expire_date
                user_module.save()
            elif user_module and not accessed:  # 存在，且设置为不可登录,改变有效时间为2000-01-01
                user_module.expire_date = datetime.datetime.strptime('2000-01-01', '%Y-%m-%d')
                user_module.save()
            elif not user_module and accessed:  # 不存在，且设置为可登录，创建数据库记录
                user_module = UserToModule(
                    user_id=int(uid),
                    module_id=int(module_id)
                )
                user_module.save()
            else:  # 不存在，且设置为不可登录(一般不存在这种情况), 直接忽略
                pass
            message = '设置成功！'
            status_code = 200
            data = {'expire_date': datetime.datetime.strftime(user_module.expire_date, '%Y-%m-%d')}
        except Exception as e:
            message = str(e)
            status_code = 400
            data = {'expire_date': ''}
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


# 用户品种权限视图
class UserToVarietyView(View):
    # 获取当前品种并标记当前用户可进入情况
    def get(self, request, uid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            operate_user = User.objects.get(id=int(uid))
            print(operate_user)
            # 当前组下的所有品种
            body_data = json.loads(request.body)
            operate_group_id = int(body_data.get('group_id'))
            all_variety = Variety.objects.all()
            if operate_group_id != 0:  # 非全部
                all_variety = all_variety.filter(group_id=operate_group_id)
            # 如果是运营人员，直接返回结果品种，并且是都可进入的
            if operate_user.is_operator:
                data = list()
                for variety in all_variety:
                    data.append({
                        'id': variety.id,
                        'name': variety.name,
                        'group': variety.group.name,
                        'accessed': 1,
                        'expire_date': '3000-01-01'
                    })
            else:
                # 当前用户有权限的品种
                accessed_varieties = UserToVariety.objects.filter(user=operate_user,
                                                                  expire_date__gt=datetime.date.today())  # 第三关系表的实例
                # 序列化
                serializer = VarietiesToUserSerializer(accessed_varieties=accessed_varieties, instance=all_variety, many=True)
                data = serializer.data
            message = '获取品种信息成功!'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
            data = []
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

    # 修改部分信息，可操作，有效期
    def patch(self, request, uid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_operator:
                raise ValueError('还没登录或不能进行这项操作!')
            # 获取当前操作的用户
            operate_user = User.objects.get(id=int(uid))
            if operate_user.is_operator:  # 用户是运营管理的人员不支持修改可操作或有效期状态
                raise ValueError('该人员不支持这项设置,请确认人员身份!')
            # 获取可操作状态
            body_data = json.loads(request.body)
            variety_id = body_data.get('variety_id', None)
            if not variety_id:
                raise ValueError('未指定的操作项目.')
            # 查询记录是否存在
            user_variety = UserToVariety.objects.filter(user_id=int(uid), variety_id=int(variety_id)).first()
            accessed = body_data.get('accessed', None)
            expire_date = body_data.get('expire_date', None)
            expire_date = datetime.datetime.strptime(expire_date, '%Y-%m-%d')
            if user_variety and accessed:  # 存在，且设置为可操作,改变有效时间
                user_variety.expire_date = expire_date
                user_variety.save()
            elif user_variety and not accessed:  # 存在，且设置为不可操作,改变有效时间为2000-01-01
                user_variety.expire_date = datetime.datetime.strptime('2000-01-01', '%Y-%m-%d')
                user_variety.save()
            elif not user_variety and accessed:  # 不存在，且设置为可操作，创建数据库记录
                user_variety = UserToVariety(
                    user_id=int(uid),
                    variety_id=int(variety_id)
                )
                user_variety.save()
            else:  # 不存在，且设置为不可操作(一般不存在这种情况), 直接忽略
                pass
            message = '设置成功！'
            status_code = 200
            data = {'expire_date': datetime.datetime.strftime(user_variety.expire_date, '%Y-%m-%d')}
        except Exception as e:
            message = str(e)
            status_code = 400
            data = {'expire_date': ''}
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )
