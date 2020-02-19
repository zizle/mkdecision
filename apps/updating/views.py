# _*_ coding:utf-8 _*_
# Author: zizle
import os
import json
import hashlib
from configparser import ConfigParser
from django.conf import settings
from django.views import View
from django.http.response import HttpResponse, StreamingHttpResponse


class CheckVersionView(View):
    update_list = dict()

    def get(self, request):
        client_v = str(request.GET.get('version', None))
        identify = int(request.GET.get('identify', 0))
        if identify:
            conf_path = os.path.join(settings.CLIENT_UPDATE_PATH, 'INSIDE/client_info.ini')
            ready_path = os.path.join(settings.CLIENT_UPDATE_PATH, 'INSIDE/')
        else:
            conf_path = os.path.join(settings.CLIENT_UPDATE_PATH, 'OUTSIDE/client_info.ini')
            ready_path = os.path.join(settings.CLIENT_UPDATE_PATH, 'OUTSIDE/')
        # 获取服务端版本
        conf = ConfigParser()
        # print(conf_path)
        conf.read(conf_path)
        server_version = str(conf.get('VERSION', 'VERSION'))
        data = {
            'version': client_v,
            'update': False,
            'file_list': {}
        }
        if client_v != server_version:
            data['version'] = server_version
            data['update'] = True
            self.find_files(ready_path, ready_path)
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
            b = f.read(8192)
            if not b:
                break
            myHash.update(b)
        f.close()
        return myHash.hexdigest()

    # 查找文件清单
    def find_files(self, path, replace_str):
        fsinfo = os.listdir(path)
        for fn in fsinfo:
            temp_path = os.path.join(path, fn)
            if not os.path.isdir(temp_path):
                # print('文件路径: {}'.format(temp_path))
                file_md5 = self.getfile_md5(temp_path)
                # print(fn)
                fn = temp_path.replace(replace_str, '')
                fn = '/'.join(fn.split('\\'))
                self.update_list[fn] = file_md5
            else:
                self.find_files(temp_path, replace_str)


# 下载文件
class DownLoadClientFile(View):
    def get(self, request):
        body_data = json.loads(request.body)
        identify = body_data.get('identify', False)
        request_file = body_data.get('filename', '')
        filename = os.path.split(request_file)[1]
        if identify:
            file_path = os.path.join(settings.CLIENT_UPDATE_PATH + 'INSIDE/', request_file)
        else:
            file_path = os.path.join(settings.CLIENT_UPDATE_PATH + 'OUTSIDE/', request_file)
        try:
            response = StreamingHttpResponse(self.file_iterator(file_path))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
        except Exception as e:
            return HttpResponse(
                content=json.dumps({"message": '下载文件失败...', "data": str(e)}),
                content_type="application/json; charset=utf-8",
                status=400
            )
        return response

    # 文件生成器
    @staticmethod
    def file_iterator(file_path, chunk_size=4096):
        # print('打开文件:', file_path)
        with open(file_path, mode='rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break