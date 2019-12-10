# _*_ coding:utf-8 _*_
# __Author__： zizle
import json
import datetime
from django.views.generic import View
from django.http.response import HttpResponse
from basic.models import Client
from utils.client import get_client
from .models import UserToModule, UserToClient
from .serializers import ClientsToUserSerializer
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
        elif mid == 0:  # 首页(0),任何都有权限
            return HttpResponse(
                content=json.dumps({"message": "通过", "data": {'permission': 1}}),
                content_type="application/json; charset=utf-8",
                status=200
            )
        # 其他普通模块的验证
        else:
            try:
                if not user:
                    raise ValueError('您还没登录或登录已过期\n请先登录再进行操作!')
                user_to_module = None
                if not user.is_researcher:  # 非内部人员查询权限
                    # 查询用户可进入的当前模块（不存在则直接报错）
                    user_to_module = UserToModule.objects.get(
                        user_id=user.id,
                        module_id=int(mid),
                    )
                # 存在则查看有效期
                if user_to_module:
                    if user_to_module.expire_date and user_to_module.expire_date < datetime.datetime.now():
                        raise ValueError('您还不能查看此功能，\n若已登录请联系管理员开放！')
                data = {'permission': 1}
                error = False
                message = '通过'
            except UserToModule.DoesNotExist:
                message = '您还不能查看此功能，\n若已登录请联系管理员开放！'
                data = {'permission': 0}
                error = True
            except Exception as e:
                message = str(e)
                data = {'permission': 0}
                error = True
            return HttpResponse(
                content=json.dumps({"message": message, 'error': error, "data": data}),
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
            accessed_clients = UserToClient.objects.filter(user=operate_user)  # 第三关系表的实例
            # 所有有效的客户端
            all_clients = Client.objects.filter(is_active=True, **body_data)
            # 序列化
            serializer = ClientsToUserSerializer(accessed_clients=accessed_clients, instance=all_clients, many=True)
            print(operate_user)
            body_data = json.loads(request.body)
            print(body_data)
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
