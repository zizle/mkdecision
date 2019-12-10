# _*_ coding:utf-8 _*_
# __Author__： zizle
import jwt
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from user.models import User


# 验证用户的中间件
class AuthenticatedUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print('请求进入')
        # 获取JWT
        token = request.META.get('HTTP_AUTHORIZATION', '')
        if not token:
            user = None
        else:
            # 验证JWT
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])  # 过期也会抛出错误
                # 查询用户
                user = User.objects.get(phone=payload['phone'], is_active=True)
            except User.DoesNotExist:
                user = None
            except Exception as e:
                print(e)
                # jwt验证失败就会抛出相应错误
                user = None
        # request对象绑定user
        request.user = user

    def process_response(self, request, response):
        print('请求结束')
        return response
