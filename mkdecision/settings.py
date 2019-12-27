# _*_ coding:utf-8 _*_
import os
import sys
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))  # 加入apps的导包路径


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y96w=styr#1%r4z3h234_$n)oyesk()_u$ofgg*q$7nrib@pnn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# 允许访问的地址
ALLOWED_HOSTS = ['*', ]

INSTALLED_APPS = [
    'django.contrib.auth',  # 验证模块
    'django.contrib.contenttypes',  # 验证模块的依赖模块
    'django.contrib.staticfiles',  # 静态文件
    'rest_framework',  # 框架用于序列化
    'user.apps.UserConfig',  # 用户
    'basic.apps.BasicConfig',  # 基础信息
    'limit.apps.LimitConfig',  # 权限管理
    'home.apps.HomeConfig',  # 首页
    'info_service.apps.InfoServiceConfig',  # 产品服务
    'trend.apps.TrendConfig',  # 数据分析
]
"""
中间件功能介绍
CommonMiddleware：
    1 可通过设置用户代理字符串进列表 DISALLOWED_USER_AGENTS=[]拒绝访问
    2 规范化URL:
        设置APPEND_SLASH=True(默认也为True) 进行URL末尾缺少'/'补全;
        设置PREPEND_WWW=True(默认False)补全www;
        设置Content-Length非流式响应的标头。
SecurityMiddleware：   
    1 请求/响应周期提供了一些安全性增强
"""
# from django.contrib.auth.middleware import AuthenticationMiddleware
MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',  # 文档强烈建议安装此中间件
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 自写,验证用户中间件
    'utils.middleware.AuthenticatedUserMiddleware',
]
# 根路径配置文件
ROOT_URLCONF = 'mkdecision.urls'
# 模板设置(前后端分离,不作设置)
TEMPLATES = [
    # {
    #     'BACKEND': 'django.template.backends.django.DjangoTemplates',
    #     'DIRS': [os.path.join(BASE_DIR, 'templates')]
    #     ,
    #     'APP_DIRS': True,
    #     'OPTIONS': {
    #         'context_processors': [
    #             'django.template.context_processors.debug',
    #             'django.template.context_processors.request',
    #             'django.contrib.auth.context_processors.auth',
    #             'django.contrib.messages.context_processors.messages',
    #         ],
    #     },
    # },
]

WSGI_APPLICATION = 'mkdecision.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.mkdecision'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
# 密码强度验证器
AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True  # 是否应启用Django的翻译系统， False 将进行一些优化，以免加载翻译机制。

USE_L10N = True  # 是否启用数据本地化格式。使用当前语言环境的格式显示数字和日期。

USE_TZ = False

# json web token有效时间(单位/秒)
JSON_WEB_TOKEN_EXPIRE = 7200

# 系统文件存储的根路径,模型中使用upload_to的路径相对于本路径下
MEDIA_ROOT = 'E:/mkDecision/'
# MEDIA_ROOT = '/Users/zizle/Desktop/CODES/static/mkDecision/'

# 静态文件
STATIC_URL = "/mkDecision/"
STATICFILES_DIRS = [
    "E:/mkDecision/",
    # "/Users/zizle/Desktop/CODES/static/mkDecision/"
]

# 指定用户模型
AUTH_USER_MODEL = 'user.User'
# 默认的有效期时间
DEFAULT_EXPIRE_DATE = datetime.datetime.strptime('3000-01-01', '%Y-%m-%d')
# 设置ENV变量，防止出现System Error
PYDEVD_USE_FRAME_EVAL = False
