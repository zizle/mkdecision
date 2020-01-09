# _*_ coding:utf-8 _*_
# __Author__： zizle
import re
import json
import datetime
from django.db import transaction
from django_redis import get_redis_connection
from django.views.generic import View
from django.http.response import HttpResponse
from .models import User
from .serializers import UserSerializer
from basic.models import Client
from limit.models import UserToClient
from utils.client import get_client
from utils.auth import user_entered, generate_jwt, get_actions_with_user


# 超级管理员视图【唯一】
class SuperUserView(View):
    def post(self, request):
        try:
            machine_code = request.GET.get('mc', None)
            if not machine_code:
                raise ValueError('缺少机器码')
            body_data = json.loads(request.body)
            password = body_data.get('password', None)
            if not password:
                raise ValueError('请设置密码')
            exist_superuser = User.objects.filter(is_superuser=True).first()
            if exist_superuser:
                raise ValueError('已存在超管:' + exist_superuser.phone)
            # 数据库事务
            with transaction.atomic():
                superuser = User.objects.create_superuser(
                    username=body_data.get('username', None),
                    email=body_data.get('email', ''),
                    phone=body_data.get('phone', None),
                    note=body_data.get('note', None),
                    password=password,
                    is_superuser=True,
                    is_operator=True,
                    is_collector=True,
                    is_researcher=True
                )
                # 创建超级管理员可登录的客户端
                client = get_client(machine_code)
                if not client:
                    client = Client(
                        name='超管客户端',
                        machine_code=machine_code,
                        is_manager=True,
                    )
                else:
                    client.is_manager = True
                client.save()
                user_to_client = UserToClient(
                    user=superuser,
                    client=client
                )
                user_to_client.save()
        except Exception as e:
            return HttpResponse(
                content=json.dumps({"message": str(e), "data": {}}),
                content_type="application/json; charset=utf-8",
                status=400
            )
        return HttpResponse(
            content=json.dumps({"message": '创建超级管理员成功!', "data": {}}),
            content_type="application/json; charset=utf-8",
            status=201
        )


# 用户登录(包含超级管理员的登录)
class UserLoginView(View):
    def post(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        # 登录
        try:
            if not client:
                raise ValueError('INVALID CLIENT!')
            body_data = json.loads(request.body)
            phone = body_data.get("phone", None)
            password = body_data.get("password", None)
            if not re.match(r'^[1][3-9][0-9]{9}$', phone):
                raise ValueError('手机号格式有误')
            user = User.objects.get(phone=phone, is_active=True)
            if not user.check_password(password):
                raise ValueError('用户名或密码错误.')
        except User.DoesNotExist:
            return HttpResponse(
                content=json.dumps({"message": '无效用户.', "error": True, "data": {}}),
                content_type="application/json; charset=utf-8",
                status=400
            )
        except Exception as e:
            return HttpResponse(
                content=json.dumps({"message": str(e), "error": True, "data": {}}),
                content_type="application/json; charset=utf-8",
                status=400
            )
        # 验证能否登录客户端
        if user_entered(user, client):
            # 更新登录时间
            user.last_login = datetime.datetime.now()
            user.save()
            # 检验通过签发json web token 登录成功
            serializer = UserSerializer(instance=user)
            data = serializer.data
            data['Authorization'] = generate_jwt(user)  # token
            data['actions'] = get_actions_with_user(user, client)  # 获取管理员可操作的模块
            message = '登录成功'
            error = False
            status_code = 200
        else:
            message = '您的账号不能在此客户端登录.\n如有需要,请联系管理员申请.'
            error = False
            status_code = 400
            data = {}
        return HttpResponse(
            content=json.dumps({"message": message, 'error': error, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


# 登录状态保持(自动登录)
class UserKeepOnline(View):
    def get(self, request):
        user = request.user
        if not user:
            return HttpResponse(
                content=json.dumps({"message": '登录信息已过时', "error": False, "data": {}}),
                content_type="application/json; charset=utf-8",
                status=400
            )
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        if not client:
            return HttpResponse(
                content=json.dumps({"message": 'INVALID CLIENT!', "error": True, "data": {}}),
                content_type="application/json; charset=utf-8",
                status=400
            )
        # 重新验证用户可登录权限
        if user_entered(user, client):
            # 更新登录时间
            user.last_login = datetime.datetime.now()
            user.save()
            # 返回用户信息
            serializer = UserSerializer(instance=user)
            data = serializer.data
            data['Authorization'] = request.META.get('HTTP_AUTHORIZATION', '')
            data['actions'] = get_actions_with_user(user, client)  # 获取管理员可操作的模块
            return HttpResponse(
                content=json.dumps({"message": '自动登录成功', 'error': False, "data": data}),
                content_type="application/json; charset=utf-8",
                status=200
            )
        else:
            return HttpResponse(
                content=json.dumps({"message": '您不能在此客户端登录', 'error': False, "data": {}}),
                content_type="application/json; charset=utf-8",
                status=400
            )


#  用户视图(根据过滤条件获取相应用户)
class UsersView(View):
    def get(self, request):
        machine_code = request.GET.get('mc', '')
        client = get_client(machine_code)
        user = request.user
        if not user or not client or not user.is_operator or not client.is_manager:
            all_users = User.objects.none()
        else:
            body_data = json.loads(request.body)
            all_users = User.objects.filter(**body_data).exclude(is_superuser=True)  # 根据需求获取用户(去除超级管理员)
        serializer = UserSerializer(instance=all_users, many=True)
        return HttpResponse(
            content=json.dumps({"message": '获取用户列表成功!', "error": False, "data": serializer.data}),
            content_type="application/json; charset=utf-8",
            status=200
        )

    # 注册普通用户
    def post(self, request):
        machine_code = request.GET.get('mc')
        client = get_client(machine_code)
        try:
            if not client:
                raise ValueError('INVALID CLIENT.')
            body_data = json.loads(request.body)
            password = body_data.get('password', None)
            if not password:
                raise ValueError('请设置密码')
            phone = body_data.get('phone', None)
            if not phone or not re.match(r'^[1][3-9][0-9]{9}$', phone):
                raise ValueError('请输入正确的手机号')
            # 获取保存在redis中的验证码验证码图片验证码
            image_code_id = body_data.get('image_code_id', '')
            redis_conn = get_redis_connection('verify_codes')
            real_image_code_text = redis_conn.get('imgcode_%s' % image_code_id)
            if not real_image_code_text:
                raise ValueError('验证码无效!')
            image_code = body_data.get('image_code', None)
            real_image_code_text = real_image_code_text.decode()  # 从redis取出的是bytes类型
            if image_code.lower() != real_image_code_text.lower():
                raise ValueError('输入的验证码有误!')
            # 开启数据库事务
            with transaction.atomic():
                user = User.objects.create_user(
                    username=body_data.get('username', ''),
                    email=body_data.get('email', ''),
                    phone=body_data.get('phone', None),
                    password=password,
                    is_researcher=client.is_manager  # 管理端注册为研究员
                )
                # 添加可登录客户端关联表数据
                user_to_client = UserToClient(
                    user=user,
                    client=client
                )
                user_to_client.save()
        except Exception as e:
            return HttpResponse(
                content=json.dumps({"message": str(e), "data": {}}),
                content_type="application/json; charset=utf-8",
                status=400
            )
        else:
            # 更新登录时间
            user.last_login = datetime.datetime.now()
            user.save()
            # 签发token(注册即登录)
            serializer = UserSerializer(instance=user)
            data = serializer.data
            data['Authorization'] = generate_jwt(user)  # token
            data['actions'] = get_actions_with_user(user, client)  # 获取管理员可操作的模块
            return HttpResponse(
                content=json.dumps({"message": '注册成功.', "data": data}),
                content_type="application/json; charset=utf-8",
                status=201
            )


# 用户基础信息视图
class UserBaseInfoView(View):
    def get(self, request, uid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        try:
            if not client:
                raise ValueError('INVALID CLIENT.')
            user = User.objects.get(id=int(uid))
        except User.DoesNotExist:
            data = {}
            message = '该用户不存在.'
            status_code = 400
        except Exception as e:
            data = {}
            message = str(e)
            status_code = 400
        else:
            serializer = UserSerializer(instance=user)
            message = '成功'
            data = serializer.data
            status_code = 200
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

    # 修改部分信息
    def patch(self, request, uid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT.')
            if not request_user or not request_user.is_operator:
                raise ValueError('登录已过期或不能进行这个操作!')
            new_data = json.loads(request.body)
            operate_user = User.objects.get(id=int(uid))
            for key, value in new_data.items():
                if key in ['username', 'phone', 'email', 'note', 'is_active', 'is_operator', 'is_collector',
                           'is_researcher']:
                    if key == 'is_active' and operate_user.id == request_user.id:
                        raise ValueError('不能对自己做此项修改。')
                    operate_user.__setattr__(key, value)
            operate_user.save()
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
