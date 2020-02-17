# _*_ coding:utf-8 _*_
# Author: zizle
import os
import json
import hashlib
from configparser import ConfigParser
from django.conf import settings
from django.views import View
from django.http.response import HttpResponse, FileResponse


class CheckVersionView(View):
    update_list = dict()

    def get(self, request):
        import time
        time.sleep(2)
        client_v = str(request.GET.get('version', None))
        # 获取服务端版本
        conf = ConfigParser()
        conf_path = os.path.join(settings.CLIENT_UPDATE_PATH, 'client_info.ini')
        print(conf_path)
        conf.read(conf_path)
        server_version = str(conf.get('VERSION', 'VERSION'))
        data = {
            'version': client_v,
            'update': False,
            'file_list': {}
        }
        if client_v != str(server_version):
            data['version'] = server_version
            data['update'] = True
            self.find_files(settings.CLIENT_UPDATE_PATH)
            data['file_list'] = self.update_list



        return HttpResponse(
            content=json.dumps({"message": '检测版本成功.', "data": data}),
            content_type="application/json; charset=utf-8",
            status=200
        )

    # 计算文件MD5
    def getfile_md5(self, filename):
        if not os.path.isfile(filename):
            return
        myHash = hashlib.md5()
        f = open(filename, 'rb')
        while True:
            b = f.read(8096)
            if not b:
                break
            myHash.update(b)
        f.close()
        return myHash.hexdigest()

    # 查找文件清单
    def find_files(self, path):
        fsinfo = os.listdir(path)
        for fn in fsinfo:
            temp_path = os.path.join(path, fn)
            if not os.path.isdir(temp_path):
                # print('文件路径: {}'.format(temp_path))
                file_md5 = self.getfile_md5(temp_path)
                # print(fn)
                fn = temp_path.replace(settings.CLIENT_UPDATE_PATH, '')
                self.update_list[fn] = file_md5
            else:
                self.find_files(temp_path)


# 下载文件
class DownLoadClientFile(View):
    def get(self, request):
        body_data = json.loads(request.body)
        filename = body_data.get('filename', None)
        file_path = os.path.join(settings.CLIENT_UPDATE_PATH, filename)
        with open(file_path, 'rb') as file:
            file = open(file_path, 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="BatchPayTemplate.xls"'
            return response