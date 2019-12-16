# _*_ coding:utf-8 _*_
# __Author__： zizle
import json
import os
from django.conf import settings
from django.views.generic import View
from django.http.response import HttpResponse
from .forms import NewsBulletinForm, AdvertisementForm
from .models import NewsBulletin, Advertisement
from .serializers import NewsBulletinSerializer, AdvertisementSerializer
from utils.client import get_client


# 新闻公告视图
class NewsBulletinView(View):
    def get(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        if not client:
            news = NewsBulletin.objects.none()
        else:
            news = NewsBulletin.objects.all()
        serializer = NewsBulletinSerializer(instance=news, many=True)
        return HttpResponse(
            content=json.dumps({"message": '获取公告数据成功!', "data": serializer.data}),
            content_type="application/json; charset=utf-8",
            status=200
        )

    def post(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_operator:
                raise ValueError('还未登录或不能进行这项操作!')
            title = request.POST.get('title', None)
            if not title:
                raise ValueError('请输入公告标题!')
            file = request.FILES
            if file:
                # 组织好数据
                data_to_save = {
                    'title': title,
                    'creator': request_user.id,
                    'content': '',
                }
                form = NewsBulletinForm(data_to_save, request.FILES)
                if form.is_valid():
                    form.save()
                    message = '上传文件成功!'
                    status_code = 201
                else:
                    raise ValueError(form.errors)
            else:

                content_text = request.POST.get('content', None)
                if not content_text:
                    raise ValueError('请输入公告内容!')
                news = NewsBulletin(
                    title=title,
                    creator_id=request_user.id,
                    content=content_text
                )
                news.save()
                message = '上传成功!'
                status_code = 201
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": {}}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


# 单个新闻公告视图
class NewsBulletinRetrieveView(View):
    def get(self, request, nid):
        # 获取当前公告数据返回
        try:
            news = NewsBulletin.objects.get(id=int(nid))
            serializer = NewsBulletinSerializer(instance=news)
            data = serializer.data
            message = '获取公告成功!'
            status_code = 200
        except NewsBulletin.DoesNotExist:
            message = '当前公告不存在!'
            status_code = 400
            data ={}
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

    def delete(self, request, nid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_operator:
                raise ValueError('还没登录或不能进行这项操作!')
            news = NewsBulletin.objects.get(id=int(nid))
            if news.file:  # 删除原文件
                file_path = settings.MEDIA_ROOT + news.file.name
                os.remove(file_path)
            news.delete()
            status_code = 200
            message = '删除公告成功!'
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": {}}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


# 广告视图
class AdvertiseView(View):
    def get(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        if not client:
            ads = Advertisement.objects.none()
        else:
            ads = Advertisement.objects.all()
        serializer = AdvertisementSerializer(instance=ads, many=True)
        return HttpResponse(
            content=json.dumps({"message": '获取广告数据成功!', "data": serializer.data}),
            content_type="application/json; charset=utf-8",
            status=200
        )

    def post(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_operator:
                raise ValueError('还未登录或不能进行这项操作!')
            name = request.POST.get('name', None)
            if not name:
                raise ValueError('请输入广告标题!')
            files = request.FILES
            if files:
                # 组织好数据
                data_to_save = {
                    'name': name,
                    'creator': request_user.id,
                    'content': request.POST.get('content', ''),
                }
                form = AdvertisementForm(data_to_save, request.FILES)
                if form.is_valid():
                    form.save()
                else:
                    raise ValueError(form.errors)
            message = '上传成功!'
            status_code = 201
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": {}}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


# 单个广告视图
class AdvertiseRetrieveView(View):
    def get(self, request, aid):
        # 获取当前广告数据返回
        try:
            ad = Advertisement.objects.get(id=int(aid))
            serializer = AdvertisementSerializer(instance=ad)
            data = serializer.data
            message = '获取广告成功!'
            status_code = 200
        except NewsBulletin.DoesNotExist:
            message = '当前广告不存在!'
            status_code = 400
            data = {}
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

    def delete(self, request, aid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_operator:
                raise ValueError('还没登录或不能进行这项操作!')
            advertisement = Advertisement.objects.get(id=int(aid))
            # 删除图片
            image_path = settings.MEDIA_ROOT + advertisement.image.name
            os.remove(image_path)
            if advertisement.file:  # 删除原文件
                file_path = settings.MEDIA_ROOT + advertisement.file.name
                os.remove(file_path)
            advertisement.delete()
            status_code = 200
            message = '删除广告成功!'
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": {}}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


# 使用图片名称找到广告
class AdvertiseWithNameView(View):
    def get(self, request, name):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        if not client:
            return HttpResponse(
                content=json.dumps({"message": 'INVALID CLIENT!', "data": {}}),
                content_type="application/json; charset=utf-8",
                status=400
            )
        image = 'home/advertisement/image/' + name
        try:
            ad = Advertisement.objects.get(image=image)
            serializer = AdvertisementSerializer(instance=ad)
            message = '获取数据成功!'
            status_code = 200
            data = serializer.data
        except Advertisement.DoesNotExist:
            message = '不存在当前数据!'
            status_code = 400
            data = {}
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )



