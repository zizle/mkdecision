# _*_ coding:utf-8 _*_
# __Author__： zizle
import json
import datetime
import os
from django.conf import settings
from django.core.paginator import Paginator
from django.views.generic import View
from django.http.response import HttpResponse
from django.core.files.storage import default_storage
from .models import MessageLink, MarketAnalysis, SearchReport, TopicSearch
from .serializers import MessageLinkSerializer, MarketAnalysisSerializer, SearchReportSerializer
from .forms import MarketAnalysisForm, SearchReportForm, TopicSearchForm
from utils.client import get_client


# 制度考核
class InstExamineView(View):
    def post(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_operator:
                raise ValueError('登录已过期或不能进行这项操作!')
            file_path = settings.MEDIA_ROOT + 'info/instExamine/产品服务_制度考核.pdf'
            default_storage.delete(file_path)  # 删除原来的文件
            # 获取文件保存
            default_storage.save(file_path, request.FILES.get('file'))
            message = '上传成功!'
            status_code = 201
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({'message': message, 'data': []}),
            content_type='application/json charset=utf-8',
            status=status_code
        )


# 部门组建
class DeptBuildView(View):
    def post(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_operator:
                raise ValueError('登录已过期或不能进行这项操作!')
            file_path = settings.MEDIA_ROOT + 'info/deptBuild/产品服务_部门组建.pdf'
            default_storage.delete(file_path)  # 删除原来的文件
            # 获取文件保存
            default_storage.save(file_path, request.FILES.get('file'))
            message = '上传成功!'
            status_code = 201
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({'message': message, 'data': []}),
            content_type='application/json charset=utf-8',
            status=status_code
        )


# 人才培养
class PersonTrainView(View):
    def post(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_operator:
                raise ValueError('登录已过期或不能进行这项操作!')
            file_path = settings.MEDIA_ROOT + 'info/personTra/产品服务_人才培养.pdf'
            default_storage.delete(file_path)  # 删除原来的文件
            # 获取文件保存
            default_storage.save(file_path, request.FILES.get('file'))
            message = '上传成功!'
            status_code = 201
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({'message': message, 'data': []}),
            content_type='application/json charset=utf-8',
            status=status_code
        )


# 专题研究
class TopicSearchView(View):
    def get(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        current_page = request.GET.get('page', 1)
        if not client:
            instances = TopicSearch.objects.none()
        else:
            instances = TopicSearch.objects.all().order_by('-update_time')
        # 分页
        paginator = Paginator(object_list=instances, per_page=25)
        try:
            page_list = paginator.get_page(current_page)
            serializer = SearchReportSerializer(instance=page_list, many=True)
            data = dict()
            data['contacts'] = serializer.data
            data['total_page'] = paginator.num_pages
            message = '获取专题研究文件信息成功'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
            data = {}
        return HttpResponse(
            content=json.dumps({'message': message, 'data': data}),
            content_type='application/json charset=utf-8',
            status=status_code
        )

    def post(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_collector:
                raise ValueError('登录已过期或不能进行这项操作!')
            file_name = request.POST.get('name', '')
            if not file_name:
                file_name = request.FILES.name
            # 组织好数据
            data_to_save = {
                'name': file_name,
                'creator': request_user.id,
            }
            form = TopicSearchForm(data_to_save, request.FILES)
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
            content=json.dumps({'message': message, 'data': []}),
            content_type='application/json charset=utf-8',
            status=status_code
        )


# 单个专题研究视图
class TopicSearchRetrieveView(View):
    def delete(self, request, sid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_collector:
                raise ValueError('登录已过期!或不能进行这个操作！')
            instance = TopicSearch.objects.get(id=int(sid))
            if not request_user.is_operator and instance.creator.id != request_user.id:
                raise ValueError('请不要删除他人上传的信息!')
            instance.delete()
            # 删除文件
            file_path = settings.MEDIA_ROOT + instance.file.name
            os.remove(file_path)
            message = '删除成功！'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({'message': message, 'data': []}),
            content_type='application/json charset=utf-8',
            status=status_code
        )


# 调研报告
class SearchReportView(View):
    def get(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        current_page = request.GET.get('page', 1)
        if not client:
            instances = SearchReport.objects.none()
        else:
            instances = SearchReport.objects.all().order_by('-update_time')
        # 分页
        paginator = Paginator(object_list=instances, per_page=25)
        try:
            page_list = paginator.get_page(current_page)
            serializer = SearchReportSerializer(instance=page_list, many=True)
            data = dict()
            data['contacts'] = serializer.data
            data['total_page'] = paginator.num_pages
            message = '获取调研报告文件信息成功'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
            data = {}
        return HttpResponse(
            content=json.dumps({'message': message, 'data': data}),
            content_type='application/json charset=utf-8',
            status=status_code
        )

    def post(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_collector:
                raise ValueError('登录已过期或不能进行这项操作!')
            file_name = request.POST.get('name', '')
            if not file_name:
                file_name = request.FILES.name
            # 组织好数据
            data_to_save = {
                'name': file_name,
                'creator': request_user.id,
            }
            form = SearchReportForm(data_to_save, request.FILES)
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
            content=json.dumps({'message': message, 'data': []}),
            content_type='application/json charset=utf-8',
            status=status_code
        )


# 单个调研报告视图
class SearchReportRetrieveView(View):
    def delete(self, request, sid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_collector:
                raise ValueError('登录已过期!或不能进行这个操作！')
            instance = SearchReport.objects.get(id=int(sid))
            if not request_user.is_operator and instance.creator.id != request_user.id:
                raise ValueError('请不要删除他人上传的信息!')
            instance.delete()
            # 删除文件
            file_path = settings.MEDIA_ROOT + instance.file.name
            os.remove(file_path)
            message = '删除成功！'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({'message': message, 'data': []}),
            content_type='application/json charset=utf-8',
            status=status_code
        )


# 短信通视图
class SMSLinkView(View):
    def get(self, request):
        machine_code = request.GET.get('mc', None)
        min_date = request.GET.get('min_date', None)
        client = get_client(machine_code)
        if not client:
            return HttpResponse(
                content=json.dumps({'message': '获取短信通成功!', 'data': []}),
                content_type='application/json charset=utf-8',
                status=200
            )
        # 无最小时间，请求全部
        if not min_date:
            messages = MessageLink.objects.all().order_by('-date', '-time')
        else:
            min_date = datetime.datetime.strptime(min_date, '%Y-%m-%d')
            print(min_date)
            messages = MessageLink.objects.filter(date__gte=min_date.date()).order_by('-date', '-time')
        serializer = MessageLinkSerializer(instance=messages, many=True)
        return HttpResponse(
            content=json.dumps({'message': '获取短信通成功!', 'data': serializer.data}),
            content_type='application/json charset=utf-8',
            status=200
        )

    def post(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_collector:
                raise ValueError('登录已过期或不能进行这项操作!')
            body_data = json.loads(request.body)
            content = body_data.get('content',None)
            if not content:
                raise ValueError('请输入内容！')
            date = datetime.datetime.strptime(body_data.get('date'), '%Y-%m-%d')
            time = datetime.datetime.strptime(body_data.get('time'), '%H:%M:%S')
            sms = MessageLink(
                date=date.date(),
                time=time.time(),
                content=content,
                creator=request_user
            )
            sms.save()
            message = '创建短信通成功!'
            status_code = 201
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({'message': message, 'data': []}),
            content_type='application/json charset=utf-8',
            status=status_code
        )


# 单个短信通视图
class SMSLinkRetrieveView(View):
    def get(self, request, mid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            instance = MessageLink.objects.get(id=int(mid))
            serializer = MessageLinkSerializer(instance=instance)
            data = serializer.data
            message = '获取短信通成功！'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
            data = {}
        return HttpResponse(
            content=json.dumps({'message': message, 'data': data}),
            content_type='application/json charset=utf-8',
            status=status_code
        )

    # 修改
    def put(self, request, mid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_collector:
                raise ValueError('登录已过期!或不能进行这个操作！')
            instance = MessageLink.objects.get(id=int(mid))
            if not request_user.is_operator and instance.creator.id != request_user.id:
                raise ValueError('请不要修改他人上传的信息!')
            body_data = json.loads(request.body)
            content = body_data.get('content', None)
            if not content:
                raise ValueError('请输入内容！')
            date = datetime.datetime.strptime(body_data.get('date'), '%Y-%m-%d')
            time = datetime.datetime.strptime(body_data.get('time'), '%H:%M:%S')
            instance.date = date.date()
            instance.time = time.time()
            instance.content = content
            instance.save()
            message = '修改短信通成功！'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({'message': message, 'data': {}}),
            content_type='application/json charset=utf-8',
            status=status_code
        )

    def delete(self, request, mid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_collector:
                raise ValueError('登录已过期!或不能进行这个操作！')
            instance = MessageLink.objects.get(id=int(mid))
            if not request_user.is_operator and instance.creator.id != request_user.id:
                raise ValueError('请不要删除他人上传的信息!')
            instance.delete()
            message = '删除成功！'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({'message': message, 'data': []}),
            content_type='application/json charset=utf-8',
            status=status_code
        )


# 市场分析视图
class MarketAnalysisView(View):
    def get(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        current_page = request.GET.get('page', 1)
        if not client:
            instances = MarketAnalysis.objects.none()
        else:
            instances = MarketAnalysis.objects.all().order_by('-update_time')
        # 分页
        paginator = Paginator(object_list=instances, per_page=25)
        try:
            page_list = paginator.get_page(current_page)
            serializer = MarketAnalysisSerializer(instance=page_list, many=True)
            data = dict()
            data['contacts'] = serializer.data
            data['total_page'] = paginator.num_pages
            message = '获取市场分析文件信息成功'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
            data = {}
        return HttpResponse(
            content=json.dumps({'message': message, 'data': data}),
            content_type='application/json charset=utf-8',
            status=status_code
        )

    def post(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_collector:
                raise ValueError('登录已过期或不能进行这项操作!')
            file_name = request.POST.get('name', '')
            if not file_name:
                file_name = request.FILES.name
            # 组织好数据
            data_to_save = {
                'name': file_name,
                'creator': request_user.id,
            }
            form = MarketAnalysisForm(data_to_save, request.FILES)
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
            content=json.dumps({'message': message, 'data': []}),
            content_type='application/json charset=utf-8',
            status=status_code
        )


# 单个市场分析视图
class MarketAnalysisRetrieveView(View):
    def delete(self, request, mid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_collector:
                raise ValueError('登录已过期!或不能进行这个操作！')
            instance = MarketAnalysis.objects.get(id=int(mid))
            if not request_user.is_operator and instance.creator.id != request_user.id:
                raise ValueError('请不要删除他人上传的信息!')
            instance.delete()
            # 删除文件
            file_path = settings.MEDIA_ROOT + instance.file.name
            os.remove(file_path)
            message = '删除成功！'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({'message': message, 'data': []}),
            content_type='application/json charset=utf-8',
            status=status_code
        )
