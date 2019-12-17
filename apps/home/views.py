# _*_ coding:utf-8 _*_
# __Author__： zizle
import json
import os
import datetime
from django.conf import settings
from django.views.generic import View
from django.http.response import HttpResponse
from .forms import NewsBulletinForm, AdvertisementForm, NormalReportForm
from .models import NewsBulletin, Advertisement, DataCategory, NormalReport
from .serializers import NewsBulletinSerializer, AdvertisementSerializer, DataCategorySerializer, NormalReportSerializer
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


# 数据分类视图
class DataCategoryView(View):
    def get(self, request, group):
        machine_code = request.GET.get('mc')
        client = get_client(machine_code)
        if not client or group not in [couple[0] for couple in DataCategory.GROUPS] + ['all']:
            categories = DataCategory.objects.none()
        else:
            categories = DataCategory.objects.all()
            if group != 'all':
                categories = categories.filter(group=group)
            else:
                categories.query.group_by = ['group']
                print(categories)
        serializer = DataCategorySerializer(instance=categories, many=True)
        return HttpResponse(
            content=json.dumps({"message": '获取分类成功!', "data": serializer.data}),
            content_type="application/json; charset=utf-8",
            status=200
        )

    def post(self, request, group):
        machine_code = request.GET.get('mc')
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            # 验证group
            if group not in [couple[0] for couple in DataCategory.GROUPS]:
                raise ValueError('错误的请求.')
            if not request_user or not request_user.is_operator:
                raise ValueError('登录已过期或您还不能进行这个操作!')
            body_data = json.loads(request.body)
            name = body_data.get('name', None)
            if not name:
                raise ValueError('请输入正确的分组名称!')
            # 创建分组
            category = DataCategory(
                name=name,
                group=group
            )
            category.save()
            message = '创建分类成功!'
            status_code = 201
        except Exception as e:
            message = str(e)
            status_code = 400

        return HttpResponse(
            content=json.dumps({"message": message, "data": {}}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


# 常规报告视图
class NormalReportView(View):
    def get(self, request):
        machine_code = request.GET.get('mc')
        client = get_client(machine_code)
        try:
            if not client:
                raise ValueError('INVALID CLIENT!')
            body_data = json.loads(request.body)
            category = int(body_data.get('category'))
            params = dict()
            if category == 0:
                pass
            elif category == -1:
                params['category'] = None
            else:
                params['category_id'] = category
            # 查询
            variety = int(body_data.get('variety'))
            if variety != 0:
                reports = list()
                for report in NormalReport.objects.filter(**params):
                    related_vids = [v.id for v in report.varieties.all()]
                    if variety in related_vids:
                        reports.append(report)
            else:
                reports = NormalReport.objects.filter(**params)
            serializer = NormalReportSerializer(instance=reports, many=True)
            message = '获取常规报告成功！'
            status_code = 200
            data = serializer.data
        except Exception as e:
            message = str(e)
            status_code = 400
            data = []
        return HttpResponse(
            content=json.dumps({'message': message, 'data': data}),
            content_type='application/json; charset=utf-8',
            status=status_code
        )

    def post(self, request):
        # 重新过滤组织数据
        machine_code = request.GET.get('mc', '')
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT.')
            if not request_user or not request_user.is_researcher:
                raise ValueError('未登录或不能进行这个操作!')
            file_name = request.POST.get('name', '')
            if not file_name:
                file_name = request.FILES.name
            date = request.POST.get('date', '')
            if not date:
                raise ValueError('该报告没有设置日期')
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            cid = int(request.POST.get('category_id', 0))  # 数据分类
            # 关联品种的id列表
            related_vids = eval(request.POST.get('variety_ids', 0))
            if not related_vids:
                raise ValueError('请选择所属品种!')
            # variety_instance = Variety.objects.get(id=vid)
            # if not user_accessed_variety(user, variety_instance):  # 验证用户品种权限
            #     raise ValueError('您还没这个品种权限.')
            # 组织好数据
            data_to_save = {
                'name': file_name,
                'date': date,
                'uploader': request_user.id,
                'category': cid if cid else None,
                'varieties': related_vids
            }
            form = NormalReportForm(data_to_save, request.FILES)
            if form.is_valid():
                form.save()
                message = '上传成功!'
                status_code = 201
            else:
                raise ValueError(form.errors)
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({'message': message, 'data': {}}),
            content_type='application/json; charset=utf-8',
            status=status_code
        )


# 单个常规报告视图
class NormalReportRetrieveView(View):
    def delete(self, request, rid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_operator:
                raise ValueError('还没登录或不能进行这项操作!')
            report = NormalReport.objects.get(id=int(rid))
            # 删除文件
            file_path = settings.MEDIA_ROOT + report.file.name
            os.remove(file_path)
            report.delete()
            status_code = 200
            message = '删除报告成功!'
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": {}}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )



