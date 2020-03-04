# _*_ coding:utf-8 _*_
# Author: zizle
from rest_framework import serializers

from .models import ServiceGuide, Question, Answer
from user.models import User


class ServiceGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceGuide
        fields = '__all__'


""" 讨论交流 """

# 提问者和回答者序列化器
class CommunicationerSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'avatar', 'username', 'phone')

    def get_phone(self, obj):
        phone = obj.phone
        return phone[0:3] + "****" + phone[7:11]


class QuestionSerializer(serializers.ModelSerializer):
    questioner = CommunicationerSerializer()
    create_time = serializers.DateTimeField(format('%Y-%m-%d %H:%M:%S'), read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'questioner', 'content', 'read_count', 'create_time')

class AnswerSerializer(serializers.ModelSerializer):
    answerer = CommunicationerSerializer()
    create_time = serializers.DateTimeField(format('%Y-%m-%d %H:%M:%S'), read_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'answerer', 'content', 'create_time')
