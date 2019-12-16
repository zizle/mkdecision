# _*_ coding:utf-8 _*_
# __Author__： zizle
from rest_framework import serializers
from .models import NewsBulletin, Advertisement


# 新闻公告序列化器
class NewsBulletinSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format('%Y-%m-%d'), read_only=True)
    creator = serializers.SerializerMethodField()

    class Meta:
        model = NewsBulletin
        fields = ('id', 'title', 'creator', 'file', 'content', 'create_time')

    def get_creator(self, obj):

        return obj.creator.note if obj.creator.note else obj.creator.phone[:3] + '****' + obj.creator.phone[7:]


# 广告数据序列化器
class AdvertisementSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format('%Y-%m-%d'), read_only=True)
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = ('id', 'name', 'creator', 'image', 'file', 'content', 'create_time')

    @staticmethod
    def get_creator(obj):
        return obj.creator.note if obj.creator.note else obj.creator.phone[:3] + '****' + obj.creator.phone[7:]

