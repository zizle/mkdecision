# _*_ coding:utf-8 _*_
# __Author__： zizle
from rest_framework import serializers
from .models import MessageLink, MarketAnalysis


# 短信通序列化器
class MessageLinkSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()

    class Meta:
        model = MessageLink
        fields = '__all__'

    @staticmethod
    def get_creator(obj):
        text = ''
        if obj.creator:
            if obj.creator.note:
                text = obj.creator.note
            else:
                text = obj.creator.phone[:3] + '****' + obj.creator.phone[7:]
        return text


# 市场分析序列化器
class MarketAnalysisSerializer(serializers.ModelSerializer):
    update_time = serializers.DateTimeField(format('%Y-%m-%d'), read_only=True)

    class Meta:
        model = MarketAnalysis
        fields = '__all__'
