# _*_ coding:utf-8 _*_
# Author: zizle
import os
import json
from configparser import ConfigParser
from django.conf import settings
from django.views import View
from django.http.response import HttpResponse


class CheckVersionView(View):
    def get(self, request):
        client_v = str(request.GET.get('version', None))
        # 获取服务端版本
        conf = ConfigParser()
        conf_path = os.path.join(settings.BASE_DIR, 'client_info.ini')
        print(conf_path)
        conf.read(conf_path)
        server_version = str(conf.get('VERSION', 'VERSION'))
        data = {
            'version': client_v,
            'update': False
        }
        if client_v != str(server_version):
            data['version'] = server_version
            data['update'] = True

        return HttpResponse(
            content=json.dumps({"message": '检测版本成功.', "data": data}),
            content_type="application/json; charset=utf-8",
            status=200
        )