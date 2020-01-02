# _*_ coding:utf-8 _*_
# __Author__： zizle
import datetime
from django.db import connection
from rest_framework import serializers
from basic.models import Variety
from .models import TrendTableGroup, TrendTable, VarietyChart


# 数据组序列化器(只序列化组，供品种序列化使用)
class TrendGroupForVarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendTableGroup
        exclude = ('create_time', 'update_time',)


# 品种序列化器(品种下的数据组)
class VarietyTableGroupSerializer(serializers.ModelSerializer):
    trend_table_groups = TrendGroupForVarietySerializer(many=True, read_only=True)

    class Meta:
        model = Variety
        exclude = ('create_time', 'update_time',)


# 数据表序列化器
class TrendTableSerializer(serializers.ModelSerializer):
    update_time = serializers.DateTimeField(format('%Y-%m-%d'), read_only=True)
    group = serializers.SlugRelatedField(slug_field='name', read_only=True)
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    editor = serializers.SerializerMethodField()

    class Meta:
        model = TrendTable
        exclude = ('create_time',)


    @staticmethod
    def get_end_date(obj):
        if obj.is_deleted:
            return ''
        # 查询表中最大时间
        max_date_sql = "SELECT MAX(col_0) From %s WHERE id > 1" % obj.sql_name
        with connection.cursor() as cursor:
            cursor.execute(max_date_sql)
            max_date = cursor.fetchone()[0]  # 终止时间
            return max_date[:10]

    @staticmethod
    def get_start_date(obj):
        if obj.is_deleted:
            return ''
        # 查询表中最小时间
        min_date_sql = "SELECT MIN(col_0) From %s WHERE id > 1" % obj.sql_name
        with connection.cursor() as cursor:
            cursor.execute(min_date_sql)
            min_date = cursor.fetchone()[0]  # 起始时间
            return min_date[:10]

    @staticmethod
    def get_editor(obj):
        text = ''
        if obj.editor:
            if obj.editor.note:
                text = obj.editor.note
            else:
                text = obj.editor.phone[:3] + '****' + obj.editor.phone[7:]
        return text


# 数据组含组下表序列化器  class TrendTableGroupSerializer 只是序列化组，并没有组下的表
class TrendGroupTablesSerializer(serializers.ModelSerializer):
    tables = serializers.SerializerMethodField()

    class Meta:
        model = TrendTableGroup
        exclude = ('create_time', 'update_time',)

    def get_tables(self, obj):
        serializer = TrendTableSerializer(obj.tables.filter(is_deleted=False), many=True)
        return serializer.data


# 图表信息序列化器
class ChartSerializer(serializers.ModelSerializer):
    variety = serializers.SlugRelatedField(slug_field='name', read_only=True)
    creator = serializers.SerializerMethodField()
    is_top = serializers.SerializerMethodField()
    is_show = serializers.SerializerMethodField()

    class Meta:
        model = VarietyChart
        exclude = ('create_time', 'update_time',)

    @staticmethod
    def get_creator(obj):
        text = ''
        if obj.creator:
            if obj.creator.note:
                text = obj.creator.note
            else:
                text = obj.creator.phone[:3] + '****' + obj.creator.phone[7:]
        return text

    @staticmethod
    def get_is_top(obj):
        return 1 if obj.is_top else 0

    @staticmethod
    def get_is_show(obj):
        return 1 if obj.is_show else 0
