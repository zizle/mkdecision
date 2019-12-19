# _*_ coding:utf-8 _*_
# __Author__： zizle
import json
from django.db import transaction, connection
from django.views.generic import View
from django.http.response import HttpResponse
from utils.client import get_client
from utils.auth import variety_user_accessed
from basic.models import Variety
from .models import TrendTableGroup, TrendTable
from .serializers import TrendTableGroupSerializer, VarietyTableGroupSerializer, TrendTableSerializer


# 以品种为条件获取数据组别及组下的数据表
class GroupTablesView(View):
    def get(self, request, vid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        if not client:
            groups = TrendTableGroup.objects.none()
        else:
            groups = TrendTableGroup.objects.filter(variety_id=int(vid))
        serializer = TrendTableGroupSerializer(instance=groups, many=True)
        return HttpResponse(
            content=json.dumps({"message": '获取数据组成功!', "data": serializer.data}),
            content_type="application/json; charset=utf-8",
            status=200
        )

    def post(self, request, vid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user:
                raise ValueError('还未登录，或登录已过期。')
            body_data = json.loads(request.body)
            group_name = body_data.get('group_name', None)
            if not group_name:
                raise ValueError('请输入组别名称!')
            # 查找当前操作的品种
            current_variety = Variety.objects.get(id=int(vid))
            # 验证用户的品种权限
            if not variety_user_accessed(variety=current_variety, user=request_user):
                raise ValueError('您还没有这个品种的权限!')
            # 创建分组
            group = TrendTableGroup(
                name=group_name,
                variety=current_variety
            )
            group.save()
            message = '新建数据分组成功！'
            status_code = 201
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({'message': message, 'data': {}}),
            content_type='application/json; charset=utf-8',
            status=status_code
        )


# 所有品种及其下的数据组
class VarietiesTrendGroupView(View):
    def get(self, request):
        machine_code = request.GET.get('mc', '')
        client = get_client(machine_code)
        if not client:
            varieties = Variety.objects.none()
        else:
            varieties = Variety.objects.all()
        serializer = VarietyTableGroupSerializer(instance=varieties, many=True)
        return HttpResponse(
            content=json.dumps({'message': '获取品种数据组成功', 'data': serializer.data}),
            content_type='application/json; charset=utf-8',
            status=200
        )


# 单个数据组下的数据表
class GroupRetrieveTablesView(View):
    def get(self, request, gid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        if not client:
            tables = TrendTable.objects.none()
        else:
            tables = TrendTable.objects.filter(group_id=int(gid))
        serializer = TrendTableSerializer(instance=tables, many=True)
        return HttpResponse(
            content=json.dumps({"message": '获取数据表成功！', "data": serializer.data}),
            content_type="application/json; charset=utf-8",
            status=200
        )

    # 新建数据表
    def post(self, request, gid):
        # 1 通过gid查询到组
        # 2 通过组得知是所属哪个品种的表
        # 3 通过品种和当前品种下的表数量确定数据库表名
        # 4 通过表的表头确定字段
        # 5 *数据库事务：数据库动态新建表
        # 6 *数据库事务：保存表格数据
        # 7 *数据库事务：创建表格名称的实例并保存
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT！')
            if not request_user:
                raise ValueError('还未登录或登录已过期！')
            table_group = TrendTableGroup.objects.get(id=int(gid))  # 获取新表所属的组
            attach_variety = table_group.variety  # 获取新表所属的品种
            if not variety_user_accessed(variety=attach_variety, user=request_user):  # 验证上传人的品种权限
                raise ValueError('您还没有该品种的权限！')
            body_data = json.loads(request.body)
            table_data = body_data.get('table_data', None)  # 表数据
            if not table_data:
                raise ValueError('您还没有上传任何数据！')
        except Exception as e:
            return HttpResponse(
                content=json.dumps({"message": str(e), "data": []}),
                content_type="application/json; charset=utf-8",
                status=403  # 理解请求但是拒绝执行,返回中包含错误信息
            )
        # 当前品种下的数据表数量计算
        table_count = 0
        for group in attach_variety.trend_table_groups.all():
            table_count += group.tables.count()
        # 新表在数据库中的名称
        sql_table_name = '%s_table_%d' % (attach_variety.name_en, table_count)  # 数据库新建表的名称
        column_headers = table_data['header_labels']  # 表头(存入新建表的第一行)
        # 创建sql语句
        cols = ''
        save_cols = list()
        for col in range(len(column_headers)):
            cols += ',col_%d VARCHAR(128)' % col
            save_cols.append("col_%d" % col)
        save_cols = ','.join(save_cols)  # 转为字符串(保存时表的列名)
        save_values = ''  # 保存的数据
        for count, item in enumerate(table_data['value_list']):
            if count == len(table_data['value_list']) - 1:
                save_values += str(tuple(item)) + ';'
            else:
                save_values += str(tuple(item)) + ','
        # 创建表的sql语句
        create_sql = "CREATE TABLE %s (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT%s);" % (sql_table_name, cols)
        # 保存数据的sql语句
        save_sql = "INSERT INTO %s (%s) VALUES %s" % (sql_table_name, save_cols, save_values)
        # print('创建表的语句:\n', create_sql)
        # print('保存数据的语句:\n', save_sql)
        # 开启事务
        try:
            with transaction.atomic():
                # 动态创建表并保存数据
                with connection.cursor() as cursor:
                    # 执行sql创建表语句
                    cursor.execute(create_sql)
                    # 执行sql保存数据
                    cursor.execute(save_sql)
                # 保存这张表名称到表名模型
                table = TrendTable(
                    name=body_data['table_name'],
                    group=table_group,
                    sql_name=sql_table_name,
                    creator=request_user,
                    editor=request_user
                )
                table.save()
            message = '上传成功'
            status_code = 201
            data = []
        except Exception as e:
            message = str(e)
            status_code = 400
            data = []
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )



