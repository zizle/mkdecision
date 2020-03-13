# _*_ coding:utf-8 _*_
# __Author__： zizle
from rest_framework import serializers
from .models import NewsBulletin, Advertisement, DataCategory, NormalReport, TransactionNotice, SpotCommodity, FinanceCalendar


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


# 数据分组序列化器
class DataCategorySerializer(serializers.ModelSerializer):
    group = serializers.ChoiceField(choices=DataCategory.GROUPS, source="get_group_display",
                                    read_only=True)  # 设置source="get_属性_display"即可
    class Meta:
        model = DataCategory
        fields = ('id', 'name', 'group')


# 常规报告序列化器
class NormalReportSerializer(serializers.ModelSerializer):
    varieties = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    uploader = serializers.SerializerMethodField()

    class Meta:
        model = NormalReport
        exclude = ('create_time', 'update_time',)

    @staticmethod
    def get_uploader(obj):
        if obj.uploader.note:
            text = obj.uploader.note
        else:
            text = obj.uploader.phone[:3] + '****' + obj.uploader.phone[7:]
        return text

    @staticmethod
    def get_varieties(obj):
        v_names = list()
        for v in obj.varieties.all():
            v_names.append(v.name)
        return '、'.join(v_names)

    @staticmethod
    def get_category(obj):
        return obj.category.name if obj.category else ''


# 交易通知序列化器
class TransactionNoticeSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    uploader = serializers.SerializerMethodField()

    class Meta:
        model = TransactionNotice
        exclude = ('create_time', 'update_time',)

    @staticmethod
    def get_uploader(obj):
        if obj.uploader.note:
            text = obj.uploader.note
        else:
            text = obj.uploader.phone[:3] + '****' + obj.uploader.phone[7:]
        return text

    @staticmethod
    def get_category(obj):
        return obj.category.name if obj.category else ''


# 现货报表系列化器
class SpotCommoditySerializer(serializers.ModelSerializer):
    uploader = serializers.SerializerMethodField()

    class Meta:
        model = SpotCommodity
        exclude = ('create_time', 'update_time',)

    @staticmethod
    def get_uploader(obj):
        text = ''
        if obj.uploader:
            if obj.uploader.note:
                text = obj.uploader.note
            else:
                text = obj.uploader.phone[:3] + '****' + obj.uploader.phone[7:]
        return text


# 财经日历序列化器
class FinanceCalendarSerializer(serializers.ModelSerializer):
    time = serializers.TimeField(format('%H:%M'), read_only=True)
    uploader = serializers.SerializerMethodField()

    class Meta:
        model = FinanceCalendar
        exclude = ('create_time', 'update_time',)

    @staticmethod
    def get_uploader(obj):
        text = ''
        if obj.uploader:
            if obj.uploader.note:
                text = obj.uploader.note
            else:
                text = obj.uploader.phone[:3] + '****' + obj.uploader.phone[7:]
        return text
