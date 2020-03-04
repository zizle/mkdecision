# _*_ coding:utf-8 _*_
# __Author__： zizle
import os
import json
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django_redis import get_redis_connection
from django.db import transaction, connection
from django.db.models import Count, Max
from django.conf import settings
from django.views.generic import View
from django.http.response import HttpResponse
from utils.client import get_client
from .models import Client, Module, VarietyGroup, Variety, ClientOpenRecord, ModuleOpenRecord
from .serializers import ClientSerializer, ModuleSerializer, VarietyGroupSerializer, VarietySerializer
from delivery.models import ServiceGuide
from delivery.serializers import ServiceGuideSerializer


""" 客户端记录 """


class ClientRecordView(View):
    def get(self, request):
        machine_code = request.GET.get('mc', '')
        client = get_client(machine_code)
        records = []
        if not client:
            pass
        else:
            select = {'day': connection.ops.date_trunc_sql('day', 'create_time')}
            result = ClientOpenRecord.objects.extra(select=select).values('client', 'day')\
                .annotate(day_count=Count('id')).order_by('-day')
            # 根据客户端查询
            client_id = request.GET.get('client', None)
            try:
                client_id = int(client_id)
            except Exception:
                client_id = None
            if client_id is not None:
                result = result.filter(client=client_id)

            for obj_dict in result:
                obj_dict['day'] = obj_dict['day'].strftime('%Y-%m-%d')
                obj_dict['client_name'], obj_dict['category'] = self.get_client_name(obj_dict['client'])
                records.append(obj_dict)
        return HttpResponse(
            content=json.dumps({'message': '获取记录成功', 'data': records}),
            content_type='application/json; charset=utf-8',
            status=200
        )

    @staticmethod
    def get_client_name(client_id):
        try:
            client = Client.objects.get(id=client_id)
        except Exception:
            return '', ''
        else:
            if client.name:
                name = client.machine_code + '(' + client.name + ')'
            else:
                name = client.machine_code + '(未命名)'
            return name, '管理端' if client.is_manager else '普通端'


""" 模块访问记录 """


# 模块访问记录
class ModuleOpenRecordView(View):
    obj_user = 0

    def get(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        records = []
        if not client:
            pass
        else:
            select = {'day': connection.ops.date_trunc_sql('day', 'create_time')}
            result = ModuleOpenRecord.objects.extra(select=select).values('user', 'day', 'module')\
                .annotate(day_count=Count('id')).order_by('-day')  # 最后对统计结果进行时间的倒序排列
            # result = result.filter(user__is_superuser=False)
            # 根据用户查询
            user_id = request.GET.get('user', None)
            try:
                user_id = int(user_id)
            except Exception:
                user_id = None
            if user_id is not None:
                result = result.filter(user=user_id)
            records = self.covert_obj(result.all())
        return HttpResponse(
            content=json.dumps({'message': '获取记录成功', 'data': records}),
            content_type='application/json; charset=utf-8',
            status=200
        )

    def covert_obj(self, obj_dicts):
        records = []
        for obj_dict in obj_dicts:
            obj_dict['day'] = obj_dict['day'].strftime('%Y-%m-%d')
            try:
                record = ModuleOpenRecord.objects.filter(user_id=obj_dict['user'], module_id=obj_dict['module']).first()
                if record.user.is_superuser:  # 剔除超级管理员数据
                    continue
                if record.user.note:
                    obj_dict['user_note'] = record.user.phone + '(' + record.user.note + ')'
                else:
                    obj_dict['user_note'] = record.user.phone + '(未备注)'
                obj_dict['module'] = record.module.name
            except Exception as e:
                obj_dict['user'] = ''
                obj_dict['module'] = ''
            records.append(obj_dict)
        return records


""" 验证码 """


class ImageCodeView(View):
    def get(self, request, image_code_id):
        # 获取随机颜色的函数
        def get_random_color():
            return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        # 生成一个图片对象
        img_obj = Image.new(
            'RGB',
            (90, 30),
            get_random_color()
        )
        # 在生成的图片上写字符
        # 生成一个图片画笔对象
        draw_obj = ImageDraw.Draw(img_obj)
        # 加载字体文件， 得到一个字体对象
        ttf_path = os.path.join(settings.BASE_DIR, "static/KumoFont.ttf")
        font_obj = ImageFont.truetype(ttf_path, 28)
        # 开始生成随机字符串并且写到图片上
        tmp_list = []
        for i in range(4):
            u = chr(random.randint(65, 90))  # 生成大写字母
            l = chr(random.randint(97, 122))  # 生成小写字母
            n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型
            tmp = random.choice([u, l, n])
            tmp_list.append(tmp)
            draw_obj.text((10 + 20 * i, 0), tmp, fill=get_random_color(), font=font_obj)  # 20（首字符左间距） + 20*i 字符的间距
        # 加干扰线
        width = 90  # 图片宽度（防止越界）
        height = 30
        for i in range(4):
            x1 = random.randint(0, width)
            x2 = random.randint(0, width)
            y1 = random.randint(0, height)
            y2 = random.randint(0, height)
            draw_obj.line((x1, y1, x2, y2), fill=get_random_color())
        # 加干扰点
        for i in range(25):
            draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw_obj.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())
        # 获得一个缓存区
        buf = BytesIO()
        # 将图片保存到缓存区
        img_obj.save(buf, 'png')
        # 将缓存区的内容返回给前端 .getvalue 是把缓存区的所有数据读取
        text = ''.join(tmp_list)
        # 将验证码保存到redis
        # 保存到redis
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.setex('imgcode_%s' % image_code_id, settings.IMAGE_CODE_REDIS_EXPIRES, text)
        return HttpResponse(buf.getvalue(), 'image/png')


""" 客户端相关 """


# 客户端视图
class ClientView(View):
    def get(self, request):
        machine_code = request.GET.get('mc', '')
        client = get_client(machine_code)
        user = request.user
        if not user or not client or not user.is_operator or not client.is_manager:
            all_clients = Client.objects.none()
        else:
            body_data = json.loads(request.body)
            # all_users = Client.objects.filter(**body_data).exclude(is_superuser=True)  # 根据需求获取用户(去除超级管理员)
            all_clients = Client.objects.filter(**body_data)  # 根据需求获取客户端(去除超级管理端)
        serializer = ClientSerializer(instance=all_clients, many=True)
        return HttpResponse(
            content=json.dumps({"message": '获取客户端列表成功!', "error": False, "data": serializer.data}),
            content_type="application/json; charset=utf-8",
            status=200
        )

    def post(self, request):
        try:
            body_data = json.loads(request.body)
            name = body_data.get('name', None)
            machine_code = body_data.get('machine_code', None)
            is_manager = body_data.get('is_manager', False)
            if not machine_code:
                raise ValueError('缺少【机器码】.')
            # 查询客户端存在与否
            with transaction.atomic():  # 数据库事务
                client = get_client(machine_code)
                if client:  # 存在，更新身份
                    client.is_manager = is_manager
                else:  # 不存在则创建
                    client = Client(
                        name=name,
                        machine_code=machine_code,
                        is_manager=is_manager
                    )
                client.save()
                # print('用户打开了客户端，进行记录')
                record = ClientOpenRecord(client=client)
                record.save()
            message = '创建成功.'
            status_code = 200
            data = {'machine_code': client.machine_code}
        except Exception as e:
            message = str(e)
            status_code = 400
            data = {}
        return HttpResponse(
            content=json.dumps({'message': message, 'data': data}),
            content_type='application/json; charset=utf-8',
            status=status_code
        )


# 单个客户端视图
class ClientRetrieveView(View):
    def get(self, request, cid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        try:
            if not client:
                raise ValueError('INVALID CLIENT.')
            operate_client = Client.objects.get(id=int(cid))
        except Client.DoesNotExist:
            data = {}
            message = '该客户端不存在.'
            status_code = 400
        except Exception as e:
            data = {}
            message = str(e)
            status_code = 400
        else:
            message = '获取客户端信息成功！'
            data = {
                'name': operate_client.name if operate_client.name else '',
                'machine_code': operate_client.machine_code
            }
            status_code = 200
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

    # 修改部分信息
    def patch(self, request, cid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT.')
            if not request_user or not request_user.is_operator:
                raise ValueError('登录已过期或不能进行这个操作!')
            operate_client = Client.objects.get(id=int(cid))
            if operate_client.name == u'超管客户端':
                raise ValueError('该客户端不能进行编辑!')
            new_data = json.loads(request.body)
            for key, value in new_data.items():
                if key in ['name', 'machine_code', 'is_active']:
                    operate_client.__setattr__(key, value)
            operate_client.save()
            message = '修改成功!'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": {}}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


""" 系统模块相关 """


# 系统开启时模块视图
class ModuleStartView(View):
    def get(self, request):
        print('请求系统模块')
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        module_data = list()
        if client:
            all_modules = Module.objects.filter(is_active=True, parent=None).order_by('order')  # 获取系统模块
            for module in all_modules:
                module_serializer = ModuleSerializer(instance=module)
                module_dict = module_serializer.data
                subs_serializer = ModuleSerializer(instance=module.sub_modules.filter(is_active=True).order_by('order').all(), many=True)
                module_dict['subs'] = subs_serializer.data
                module_data.append(module_dict)
        return HttpResponse(
            content=json.dumps({"message": '获取模块列表成功!', "data": module_data}),
            content_type="application/json; charset=utf-8",
            status=200
        )


# 系统模块视图
class ModuleView(View):
    def get(self, request):
        # print('请求系统模块')
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        module_data = list()
        if client:
            all_modules = Module.objects.filter(parent=None).order_by('order')  # 获取系统模块
            for module in all_modules:
                module_serializer = ModuleSerializer(instance=module)
                module_dict = module_serializer.data
                subs_serializer = ModuleSerializer(instance=module.sub_modules.order_by('order').all(), many=True)
                module_dict['subs'] = subs_serializer.data
                module_data.append(module_dict)
        return HttpResponse(
            content=json.dumps({"message": '获取模块列表成功!', "data": module_data}),
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
                raise ValueError('还没登录或不能进行这个操作!')
            body_data = json.loads(request.body)
            name = body_data.get('name', None)
            if not name:
                raise ValueError('请输入正确的名称.')
            parent = body_data.get('parent', None)  # 父级
            parent = int(parent) if parent else None
            # 查找最大的order
            max_order_dict = Module.objects.all().aggregate(Max('order'))
            current_order = 0 if not max_order_dict['order__max'] else max_order_dict['order__max']
            next_order = current_order + 1
            # 创建
            module = Module(name=name, parent_id=parent, order=next_order)
            module.save()
            data = {'id': module.id, 'name': module.name}
            message = '创建新模块成功!'
            status_code = 201
        except Exception as e:
            message = str(e)
            status_code = 400
            data = {}
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

    def patch(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_operator:
                raise ValueError('还没登录或不能进行这个操作!')
            body_data = json.loads(request.body)
            current_id = body_data.get("current_id", None)
            replace_id = body_data.get("replace_id", None)
            print(current_id, replace_id)
            if not current_id or not replace_id:
                raise ValueError('参数错误.current_id, replace_id')
            # 查询对应的模块
            current_module = Module.objects.get(id=current_id)
            replace_module = Module.objects.get(id=replace_id)
            # 交换两个order
            current_module.order, replace_module.order = replace_module.order, current_module.order
            current_module.save()
            replace_module.save()
            serializer = ModuleSerializer(instance=[current_module, replace_module], many=True)
            data = serializer.data
            message = "移动成功."
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
            data = []
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

# 单个模块基础信息视图
class ModuleRetrieveView(View):
    def get(self, request, mid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT.')
            operate_module = Module.objects.get(id=int(mid))
        except Module.DoesNotExist:
            data = {}
            message = '该模块不存在.'
            status_code = 400
        except Exception as e:
            data = {}
            message = str(e)
            status_code = 400
        else:
            message = '获取模块信息成功！'
            data = {'name': operate_module.name}
            status_code = 200
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

    # 修改部分信息
    def patch(self, request, mid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT.')
            if not request_user or not request_user.is_operator:
                raise ValueError('登录已过期或不能进行这个操作!')
            new_data = json.loads(request.body)
            operate_module = Module.objects.get(id=int(mid))
            for key, value in new_data.items():
                if key in ['name', 'is_active']:
                    operate_module.__setattr__(key, value)
            operate_module.save()
            message = '修改成功!'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": {}}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


""" 品种相关 """


# 品种组视图（含每组下的品种）
class GroupVarietiesView(View):
    def get(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        if not client:
            variety_groups = VarietyGroup.objects.none()
        else:
            variety_groups = VarietyGroup.objects.all()
        serializer = VarietyGroupSerializer(instance=variety_groups, many=True)
        return HttpResponse(
            content=json.dumps({"message": '获取品种分组成功!', "data": serializer.data}),
            content_type="application/json; charset=utf-8",
            status=200
        )

    # 新建品种分组
    def post(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_operator:
                raise ValueError('还没登录或不能进行这个操作!')
            # 新建
            body_data = json.loads(request.body)
            group = VarietyGroup(name=body_data.get('name', None))
            group.save()
            message = '新建组成功!'
            status_code = 201
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": {}}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


# 单个品种组视图
class GroupRetrieveVarietiesView(View):
    def get(self, request, gid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        try:
            if not client:
                raise ValueError('INVALID CLIENT!')
            all_variety = Variety.objects.all()
            if int(gid) != 0:
                all_variety = all_variety.filter(group_id=int(gid))
            serializer = VarietySerializer(instance=all_variety, many=True)
            message = '获取品种成功!'
            status_code = 200
            data = serializer.data
        except Exception as e:
            message = str(e)
            status_code = 400
            data = []
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

    # 在组别下新建品种
    def post(self, request, gid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user or not request_user.is_operator:
                raise ValueError('还未登录或不能进行这个操作!')
            body_data = json.loads(request.body)
            name = body_data.get('name', None)
            name_en = body_data.get('name_en', None)
            exchange_lib = body_data.get('exchange_lib', 0)
            if not all([gid, name, name_en]):
                raise ValueError('缺少【名称】或【英文代码】')
            # 创建新品种
            new_variety = Variety(
                group_id=int(gid),
                name=name,
                name_en=name_en,
                exchange=exchange_lib
            )
            new_variety.save()
            message = '新建品种成功！'
            status_code = 201
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": {}}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

    def delete(self, request, gid):
        print('删除gid', gid)
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not user or not user.is_operator:
                raise ValueError('您登录已过期或不能进行这项操作!')
            group = VarietyGroup.objects.get(id=int(gid))
            with transaction.atomic():
                # 删除此组所有品种下的所有表
                with connection.cursor() as cursor:
                    for variety in group.varieties.all():
                        for i in range(9999):
                            delete_sql = "DROP TABLE %s;" % (variety.name_en + '_table_' + str(i))
                            try:
                                cursor.execute(delete_sql)
                            except Exception:
                                break
                group.delete()
            message = '删除成功!'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": {}}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


# 单个品种详细视图
class VarietyRetrieveView(View):
    def get(self, request, vid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        try:
            if not client:
                raise ValueError('INVALID CLIENT!')
            operate_variety = Variety.objects.get(id=int(vid))
            serializer = VarietySerializer(instance=operate_variety)
            data = serializer.data
            data['all_groups'] = [{'id': g.id, 'name': g.name} for g in VarietyGroup.objects.all()] # 加入所有分组
            message = '获取品种成功!'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
            data = []
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

    # 修改信息
    def put(self, request, vid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT.')
            if not request_user or not request_user.is_operator:
                raise ValueError('登录已过期或不能进行这个操作!')
            new_data = json.loads(request.body)
            operate_variety = Variety.objects.get(id=int(vid))
            for key, value in new_data.items():
                if key in ['name', 'name_en', 'group_id']:
                    operate_variety.__setattr__(key, value)
            operate_variety.save()
            message = '修改成功!'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": {}}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


# 获取交易所及其下的所有品种
class ExchangeAndVarietyView(View):
    def get(self, request):
        # 准备交易所的英文代号,对应Variety.EXCHANGES
        exchanges = [
            {"index": 1, "name": "郑州商品交易所", "en_code": "czce"},
            {"index": 2, "name": "上海期货交易所", "en_code": "shfe"},
            {"index": 3, "name": "大连商品交易所", "en_code": "dce"},
            {"index": 4, "name": "中国金融期货交易所", "en_code": "cffex"},
            {"index": 5, "name": "上海能源交易中心", "en_code": "ine"},
        ]
        # 遍历交易所
        response_data = list()
        for exchange_item in exchanges:
            exchange_data = dict()
            exchange_data["name"] = exchange_item["name"]
            exchange_data["en_code"] = exchange_item["en_code"]
            varieties = Variety.objects.filter(exchange=exchange_item['index'])
            varieties_serializer = VarietySerializer(instance=varieties, many=True)
            exchange_data["varieties"] = varieties_serializer.data
            service_guides = ServiceGuide.objects.filter(exchange=exchange_item['index'])
            service_guide_serializer = ServiceGuideSerializer(instance=service_guides, many=True)
            exchange_data['service_guides'] = service_guide_serializer.data
            response_data.append(exchange_data)
        return HttpResponse(
            content=json.dumps({"message": "获取成功", "data": response_data}),
            content_type="application/json; charset=utf-8",
            status=200
        )

