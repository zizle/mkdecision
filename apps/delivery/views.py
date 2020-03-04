# _*_ coding:utf-8 _*_
# Author: zizle
import json
from django.http import HttpResponse
from django.views import View
from .models import Question
from .serializers import QuestionSerializer, AnswerSerializer


# 讨论交流视图
class QuestionsListView(View):
    def get(self, request):
        # .filter(~Q(questioner=None)) 过滤无用户的问题
        keyword = request.GET.get('keyword')
        flag_user = request.GET.get('user')
        print(keyword, flag_user)
        if keyword:  # 表示搜索
            print('搜索问题')
            questions = Question.objects.filter(
                content__contains=keyword).order_by('-create_time')
        elif flag_user:  # 查找用户自己的问题
            print('自己题的问题')
            user = request.user
            if not user:
                print('匿名无问题')
                questions = Question.objects.none()
            else:
                print('不匿名有问题')
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
        print(response_data)
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
            print(body_data)
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

