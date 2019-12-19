# _*_ coding:utf-8 _*_
# __Author__： zizle
import datetime
import time
import jwt
from django.conf import settings
from limit.models import UserToClient, UserToVariety


# 用户可否进入客户端
def user_entered(user, client):
    if user.is_superuser:
        return True
    try:
        user_to_client = UserToClient.objects.get(user=user, client=client)
    except UserToClient.DoesNotExist:
        return False
    # 如果存在则验证有效时间
    if user_to_client.expire_date and user_to_client.expire_date < datetime.date.today():
        return False
    else:
        return True


# 用户是否有品种的权限
def variety_user_accessed(variety, user):
    if user.is_superuser or user.is_operator:
        return True
    try:
        user_to_variety = UserToVariety.objects.get(user=user, variety=variety)
    except UserToVariety.DoesNotExist:
        return False
    # 如果存在则验证有效时间
    if user_to_variety.expire_date and user_to_variety.expire_date < datetime.date.today():
        return False
    else:
        return True


# 生成json web token
def generate_jwt(user):
    # 发布时间
    issued_at = time.time()
    expiration = issued_at + settings.JSON_WEB_TOKEN_EXPIRE
    token_dict = {
        'iat': issued_at,  # token的发布时间(时间戳)
        'exp': expiration,  # token销毁的时间(时间戳)
        'phone': user.phone
    }
    headers = {
        'alg': "HS256",  # 声明所使用的算法
    }
    # 调用jwt库,生成json web token
    jwt_token = jwt.encode(
        token_dict,  # payload, 有效载体
        settings.SECRET_KEY,  # 进行加密签名的密钥
        algorithm="HS256",  # 指明签名算法方式, 默认也是HS256
        headers=headers  # json web token 数据结构包含两部分, payload(有效载体), headers(标头)

    ).decode('utf-8')  # python3 编码后得到 bytes, 再进行解码(指明解码的格式), 得到一个str
    return jwt_token


# 根据用户身份获取模块
def get_actions_with_user(user, client):
    actions = list()
    if user.is_superuser and client.is_manager:
        actions.append({'id': -1, 'name': '数据管理'})
        actions.append({'id': -2, 'name': '运营管理'})
        actions.append({'id': -9, 'name': '权限管理'})

    elif user.is_operator and client.is_manager:
        actions.append({'id': -1, 'name': '数据管理'})
        actions.append({'id': -2, 'name': '运营管理'})

    elif user.is_collector or user.is_researcher and client.is_manager:
        actions.append({'id': -1, 'name': '数据管理'})
    else:
        pass
    return actions
