# _*_ coding:utf-8 _*_
# Author: zizle
import json
from django.db import transaction, connection
from django.http import HttpResponse
from django.views import View
from .models import Question, Answer, StoreHouse, VarietyInformation
from .serializers import QuestionSerializer, AnswerSerializer, StorehouseSerializer
from basic.models import Variety


# 品种基本信息
class VarietyInformationView(View):
    def post(self, request):
        request_user = request.user
        if not request_user or not request_user.is_collector:
            return HttpResponse(
                content=json.dumps({'message': "您未登录或无权限执行此操作.", 'data': {}}),
                content_type='application/json; charset=utf-8',
                status=400
            )
        try:
            body_data = json.loads(request.body)
            # 根据内容添加多对多字段内容
            with transaction.atomic():
                for variety_info_item in body_data:
                    # 查找当前信息所属品种
                    variety = Variety.objects.get(name_en=variety_info_item['name_en'])
                    info_obj = VarietyInformation.objects.create(
                        variety=variety,
                        delivery_date=variety_info_item['delivery_date'],
                        warrant_expire_date=variety_info_item['warrant_expire_date'],
                        delivery_unit_min=variety_info_item['delivery_unit_min']
                    )
            message = "上传成功"
            status_code = 201
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({'message': message, 'data': {}}),
            content_type='application/json; charset=utf-8',
            status=status_code
        )


# 讨论交流视图,提问题视图
class QuestionsListView(View):
    def get(self, request):
        # .filter(~Q(questioner=None)) 过滤无用户的问题
        keyword = request.GET.get('keyword')
        flag_user = request.GET.get('user')
        # print(keyword, flag_user)
        if keyword:  # 表示搜索
            # print('搜索问题')
            questions = Question.objects.filter(
                content__contains=keyword).order_by('-create_time')
        elif flag_user:  # 查找用户自己的问题
            # print('自己题的问题')
            user = request.user
            if not user:
                # print('匿名无问题')
                questions = Question.objects.none()
            else:
                # print('不匿名,有问题')
                questions = Question.objects.filter(questioner=user).order_by('-create_time')
        else:
            questions = Question.objects.all().order_by('-create_time')
        response_data = list()
        for question in questions:
            answers = question.answer_set.all()
            question_serializer = QuestionSerializer(question)
            answers_serializer = AnswerSerializer(instance=answers, many=True)
            question_data = question_serializer.data
            question_data['answers'] = answers_serializer.data
            response_data.append(question_data)
        return HttpResponse(
            content=json.dumps({'message': '获取记录成功', 'data': response_data}),
            content_type='application/json; charset=utf-8',
            status=200
        )

    # 提交新建问题
    def post(self, request):
        request_user = request.user
        if not request_user:
            return HttpResponse(
                content=json.dumps({'message': "您还未登录，或登录已过期..", 'data': {}}),
                content_type='application/json; charset=utf-8',
                status=400
            )
        # 获取问题内容
        try:
            body_data = json.loads(request.body)
            content = body_data.get('content', None)
            if not content:
                raise ValueError('请输入问题描述。')
            question = Question(content=content, questioner=request_user)
            question.save()
            message = "发布成功！"
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({'message': message, 'data': {}}),
            content_type='application/json; charset=utf-8',
            status=status_code
        )


# 回答问题视图
class CreateAnswerView(View):
    def post(self, request):
        request_user = request.user
        if not request_user:
            return HttpResponse(
                content=json.dumps({'message': "您还未登录，或登录已过期..", 'data': {}}),
                content_type='application/json; charset=utf-8',
                status=400
            )
        # 获取回答内容
        try:
            body_data = json.loads(request.body)
            content = body_data.get('content', None)
            question_id = body_data.get('question_id', None)
            if not content or not question_id:
                raise ValueError('参数有误。。')
            question_id = int(question_id)
            answer = Answer(content=content, answerer=request_user,
                            question_id_id=question_id)
            answer.save()
            message = "发布成功！"
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({'message': message, 'data': {}}),
            content_type='application/json; charset=utf-8',
            status=status_code
        )


# 仓库信息
import time
class StorehouseView(View):
    def get(self, request):

        keyword = request.GET.get('keyword')

        if keyword:
            # keyword要为品种
            # 查询keyword品种
            store_set = StoreHouse.objects.none()
            for variety in Variety.objects.filter(name__contains=keyword):
                # 查询仓库并合并
                store_set = store_set | StoreHouse.objects.filter(variety=variety)
            query_set = store_set.distinct()
            serializer = StorehouseSerializer(instance=query_set, many=True)
            return HttpResponse(
                content=json.dumps({'message': "获取仓库信息成功!", 'data': serializer.data}),
                content_type='application/json; charset=utf-8',
                status=200
            )
        else:
            select_sql = "SELECT id,name,longitude,latitude FROM delivery_storehouse;"
            with connection.cursor() as cursor:
                cursor.execute(select_sql)
                houses = cursor.fetchall()
            response_data = list()
            for house_item in houses:
                house_obj = dict()
                house_obj['id'] = house_item[0]
                house_obj['name'] = house_item[1]
                house_obj['longitude'] = house_item[2]
                house_obj['latitude'] = house_item[3]
                response_data.append(house_obj)
            return HttpResponse(
                content=json.dumps({'message': "获取仓库信息成功!", 'data': response_data}),
                content_type='application/json; charset=utf-8',
                status=200
            )


    def post(self, request):
        request_user = request.user
        if not request_user or not request_user.is_collector:
            return HttpResponse(
                content=json.dumps({'message': "您未登录或无权限执行此操作.", 'data': {}}),
                content_type='application/json; charset=utf-8',
                status=400
            )
        new_storehouse = list()
        try:
            body_data = json.loads(request.body)
            # 先根据内容创建出仓库实例
            # 根据内容添加多对多字段内容
            with transaction.atomic():
                for house_item in body_data:
                    # 找出仓库对应的品种(多个)，对应的省份(一个)
                    # print(house_item)
                    # print(house_item['name'], house_item['varieties_en'], house_item['province_en'])
                    variety_list = Variety.objects.filter(name_en__in=house_item['varieties_en'])
                    if not variety_list:
                        msg = house_item["name"] + "关联品种错误." + str(house_item['varieties_en'])
                        raise ValueError(msg)
                    # for variety_en in house_item['varieties_en']:
                    #     variety_list.append(Variety.objects.get(en_code=variety_en))
                    del house_item['varieties_en']
                    del house_item['varieties']
                    # area = Area.objects.get(en_code=house_item['province_en'])
                    del house_item['province_en']
                    # del house_item['province']
                    # house_item['area'] = area.id
                    # 创建仓库模型(除多对多外的字段)
                    house = StoreHouse.objects.create(
                        province=house_item['province'],
                        name=house_item['name'],
                        house_code=house_item['house_code'],
                        arrived=house_item['arrived'],
                        premium=house_item['premium'],
                        address=house_item['address'],
                        link=house_item['link'],
                        tel_phone=house_item['tel_phone'],
                        fax=house_item['fax'],
                        longitude=house_item['longitude'],
                        latitude=house_item['latitude']
                    )
                    house.variety.set(variety_list)
                    new_storehouse.append(house)
                # response_serializer = serializers.StorehouseMaintainSerializer(instance=new_storehouse, many=True)
                # response_data = response_serializer.data
                message = "上传成功！"
                status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
                content=json.dumps({'message': message, 'data': {}}),
                content_type='application/json; charset=utf-8',
                status=status_code
            )

# 某省份下的仓库信息
class ProvinceStorehouseView(View):
    def get(self, request, province):
        storehouse_set = StoreHouse.objects.filter(province=province)
        # print(storehouse_set)
        if not storehouse_set:
            return HttpResponse(
                content=json.dumps({'message': "无相关仓库信息", 'data': {}}),
                content_type='application/json; charset=utf-8',
                status=200
            )
        # 数据结构
        """
        {'品种'：[仓库, 仓库, ...], '品种'：[仓库, 仓库, ...], }
        """
        response_data = dict()
        response_data['province'] = province
        store_count = 0  # 统计数量
        for house in storehouse_set:
            if house.variety.all():
                store_count += 1
            for variety in house.variety.all():
                if variety.name not in response_data:
                    response_data[variety.name] = list()
                response_data[variety.name].append({"id": house.id, "name": house.name, "province": house.province})
        response_data['count'] = store_count
        return HttpResponse(
            content=json.dumps({'message': "查询成功！", 'data': response_data}),
            content_type='application/json; charset=utf-8',
            status=200
        )

# 品种下的仓库信息
class VarietyStorehouseView(View):
    def get(self, request, variety):
        response_data = dict()
        exchange_dict = {
            1: "郑州商品交易所",
            2: "上海期货交易所",
            3: "大连商品交易所",
            4: "中国金融期货交易所",
            5: "上海国际能源交易中心"
        }

        try:
            # 单个品种的信息
            variety_obj = Variety.objects.get(name_en=variety)
            response_data["name"] = variety_obj.name
            response_data['name_en'] = variety_obj.name_en
            response_data['exchange'] = exchange_dict.get(variety_obj.exchange)
            # base_info = variety_obj.varietybaseinfo_set.get(is_active=True, variety=variety_obj)  # 没有foreign_key的一方查询另一方.Model_set.all()
            information_obj = variety_obj.infos.first()
            if information_obj:
                response_data['delivery_date'] = information_obj.delivery_date
                response_data['warrant_expire_date'] = information_obj.warrant_expire_date
                response_data['delivery_unit_min'] = information_obj.delivery_unit_min
            else:
                response_data['delivery_date'] = ''
                response_data['warrant_expire_date'] = ''
                response_data['delivery_unit_min'] = ''

        except Variety.DoesNotExist:
            return HttpResponse(
                content=json.dumps({'message': "无相关仓库信息", 'data': {}}),
                content_type='application/json; charset=utf-8',
                status=200
            )
        # 品种的仓库信息
        storehouses = variety_obj.storehouse_set.all()
        # storehouses.query.group_by = ['area']  # 以省分组
        storehouse_data = dict()
        storehouse_data['count'] = storehouses.count()
        for house in storehouses:
            province = house.province
            if province not in storehouse_data:
                storehouse_data[province] = list()
            storehouse_data[province].append({"id": house.id, "name": house.name, "province": house.province})
        # storehouse_serializer = serializers.StorehouseNameSerializer(instance=storehouses, many=True)
        # variety_serializer = serializers.VarietySerializer(instance=variety_obj)
        response_data['storehouses'] = storehouse_data
        return HttpResponse(
            content=json.dumps({'message': "查询仓库成功", 'data': response_data}),
            content_type='application/json; charset=utf-8',
            status=200
        )


# 单个具体仓库信息
class OneStorehouseView(View):
    def get(self, request, sid):
        try:
            house = StoreHouse.objects.get(id=int(sid))
        except Exception:
            return HttpResponse(
                content=json.dumps({'message': "无相关仓库信息", 'data': {}}),
                content_type='application/json; charset=utf-8',
                status=200
            )
        house_serializer = StorehouseSerializer(instance=house)
        # # 查找仓单数据
        # house_report = house.housereport_set.order_by('-date').all()
        # # 整理仓单数据{'品种1': [仓单1, 仓单2, 仓单3..], '品种2': [仓单1, 仓单2, 仓单3..], }
        # reports_dict = dict()
        # for report in house_report:
        #     if report.variety.name not in reports_dict:
        #         reports_dict[report.variety.name] = list()
        #     report_serializer = serializers.HouseReportSerializer(report)
        #     reports_dict[report.variety.name].append(report_serializer.data)
        house_data = house_serializer.data
        house_data['reports'] = {}
        return HttpResponse(
            content=json.dumps({'message': "获取仓库数据成功！", 'data': house_data}),
            content_type='application/json; charset=utf-8',
            status=200
        )