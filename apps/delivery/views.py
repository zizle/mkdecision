# _*_ coding:utf-8 _*_
# Author: zizle
import json
from django.db import transaction
from django.http import HttpResponse
from django.views import View
from .models import Question, Answer, StoreHouse
from .serializers import QuestionSerializer, AnswerSerializer
from basic.models import Variety


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
class StorehouseView(View):
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
            print(body_data)
            # 先根据内容创建出仓库实例
            # 根据内容添加多对多字段内容
            with transaction.atomic():
                for house_item in body_data:
                    # 找出仓库对应的品种(多个)，对应的省份(一个)
                    # print(house_item)
                    # print(house_item['name'], house_item['varieties_en'], house_item['province_en'])
                    variety_list = Variety.objects.filter(name_en__in=house_item['varieties_en'])
                    if not variety_list:
                        msg = house_item["name"] + "关联品种错误."
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
            print(e)
        return HttpResponse(
                content=json.dumps({'message': message, 'data': {}}),
                content_type='application/json; charset=utf-8',
                status=status_code
            )