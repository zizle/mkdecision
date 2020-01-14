"""
WSGI config for mkdecision project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# # 虚拟环境包位置
# virtual_dir = 'E:/Virtualenv/customerService/Lib/site-packages'
# sys.path.insert(0, virtual_dir)
# # 项目文件位置
# project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mkdecision.settings')

application = get_wsgi_application()
