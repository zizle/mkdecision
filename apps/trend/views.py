# _*_ coding:utf-8 _*_
# __Author__： zizle
import json
import datetime
from django.db import transaction, connection
from django.views.generic import View
from django.http.response import HttpResponse
from utils.client import get_client
from utils.auth import variety_user_accessed
from basic.models import Variety
from .models import TrendTableGroup, TrendTable, VarietyChart
from .serializers import TrendGroupTablesSerializer, VarietyTableGroupSerializer, TrendTableSerializer, ChartSerializer


# 以品种为条件获取数据组别
class GroupTablesView(View):
    def get(self, request, vid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        if not client:
            groups = TrendTableGroup.objects.none()
        else:
            groups = TrendTableGroup.objects.filter(variety_id=int(vid))
        serializer = TrendGroupTablesSerializer(instance=groups, many=True)
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
            origin_note = body_data.get('origin_note', None)
            if not origin_note:
                raise ValueError('请标记数据来源.')
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
        create_sql = "CREATE TABLE %s (id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT%s);" % (sql_table_name, cols)
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
                    editor=request_user,
                    origin_note=origin_note
                )
                table.save()
            message = '上传成功'
            status_code = 201
            data = []
        except Exception as e:
            print(e)
            message = str(e)
            status_code = 400
            data = []
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


# 某个数据表的详细数据
class RetrieveTableView(View):
    def get(self, request, tid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        look = request.GET.get('look', False)
        try:
            if not client:
                raise ValueError('INVALID CLIENT!')
            table = TrendTable.objects.get(id=int(tid)) # 查询表资料
            if look:  # 只是查看数据
                # 查询表详情的sql语句
                query_sql = "SELECT * FROM %s WHERE id>1" % table.sql_name
                # 查询表头语句
                header_sql = "SELECT * FROM %s WHERE id=1" % table.sql_name
            else:  # 编辑数据
                request_user = request.user
                if not request_user:
                    raise ValueError('登录已过期，请重新登录！')
                # 找到对应品种,验证权限
                if not variety_user_accessed(variety=table.group.variety, user=request_user):
                    raise ValueError('你还不能进行这个品种的数据操作!')
                # 查询表详情的最后20条数据sql语句
                query_sql = "SELECT * FROM %s ORDER BY id DESC LIMIT 20" % table.sql_name
                # 查询表头数据
                header_sql = "SELECT * FROM %s WHERE id=1" % table.sql_name
            with connection.cursor() as cursor:
                cursor.execute(header_sql)
                header_data = cursor.fetchone()
                cursor.execute(query_sql)
                table_data = cursor.fetchall()  # 起始时间
                data = {
                    'header_data': header_data,
                    'table_data': table_data,
                }
                message = '获取表数据成功！'
                status_code = 200
        except Exception as e:
            data = {'header_data':[],'table_data':[]}
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

    def post(self, request, tid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client:
                raise ValueError('INVALID CLIENT!')
            table = TrendTable.objects.get(id=int(tid))  # 查询表资料
            if not request_user:
                raise ValueError('登录已过期，请重新登录！')
            # 找到对应品种,验证权限
            if not variety_user_accessed(variety=table.group.variety, user=request_user):
                raise ValueError('你还不能进行这个品种的数据操作!')
            body_data = json.loads(request.body)
            # 增加数据
            col_count = len(body_data['value_list'][0])
            save_values = ''  # 保存的数据
            for count, item in enumerate(body_data['value_list']):
                if count == len(body_data['value_list']) - 1:
                    save_values += str(tuple(item)) + ';'
                else:
                    save_values += str(tuple(item)) + ','

            # 保存时表的列名
            cols = ''
            save_cols = list()
            for col in range(col_count):
                cols += ',col_%d' % col
                save_cols.append("col_%d" % col)
            save_cols = ','.join(save_cols)  # 转为字符串(保存时表的列名)
            # 保存数据的sql语句
            save_sql = "INSERT INTO %s (%s) VALUES %s" % (table.sql_name, save_cols, save_values)
            print(save_sql)
            with connection.cursor() as cursor:
                cursor.execute(save_sql)
            message = '新增表数据成功！'
            status_code = 201
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": []}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

    # 删除表或删除表内的某一个记录
    def delete(self, request, tid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client:
                raise ValueError('INVALID CLIENT!')
            if not request_user:
                raise ValueError('登录已过期，请重新登录!')
            table = TrendTable.objects.get(id=int(tid))  # 查询表资料
            # 找到对应品种,验证权限
            if not variety_user_accessed(variety=table.group.variety, user=request_user):
                raise ValueError('你还不能进行这个品种的数据操作!')
            body_data = json.loads(request.body)
            delete_all = body_data.get('operate', None)
            if delete_all != 'all':  # 删除某个数据
                row_id = body_data.get('row_id', 0)
                if not row_id:
                    raise ValueError('删除数据出错！')
                # 删除数据的sql语句
                delete_sql = "DELETE FROM %s WHERE id=%s" % (table.sql_name, row_id)
                # 数据库事务
                with transaction.atomic():
                    with connection.cursor() as cursor:
                        cursor.execute(delete_sql)
                    table.update_time = datetime.datetime.now()
                    table.editor = request_user
                    table.save()
            else:  # 删除整张表
                if not request_user.is_operator:
                    raise ValueError('你不能删除整个表。')
                # 删除表的语句
                delete_sql = "DROP TABLE %s" % table.sql_name
                with transaction.atomic():
                    with connection.cursor() as cursor:
                        cursor.execute(delete_sql)
                    table.update_time = datetime.datetime.now()
                    table.editor = request_user
                    table.is_deleted = True
                    table.save()
            message = '删除操作成功！'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": []}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


# 品种图表
class ChartView(View):
    # 主页图表
    def get(self, request):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        if not client:
            charts = VarietyChart.objects.none()
        else:
            charts = VarietyChart.objects.filter(is_top=True, table__is_deleted=False)
        serializer = ChartSerializer(instance=charts, many=True)
        return HttpResponse(
            content=json.dumps({"message": '获取图表信息成功！', "data": serializer.data}),
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
            if not request_user:
                raise ValueError('登录已过期，请重新登录!')
            body_data = json.loads(request.body)
            table_id = body_data.get('table_id', None)
            if not table_id:
                raise ValueError('未找到当前表!')
            # 验证权限
            table = TrendTable.objects.get(id=int(table_id))  # 所属表
            variety = table.group.variety  # 所属品种
            if not variety_user_accessed(variety=variety, user=request_user):
                raise ValueError('您还没有这个品种的权限!')
            # 创建图表信息
            body_data['x_bottom'] = json.dumps(body_data['x_bottom'])
            body_data['x_bottom_label'] = json.dumps(body_data['x_bottom_label'])
            body_data['x_top'] = json.dumps(body_data['x_top'])
            body_data['x_top_label'] = json.dumps(body_data['x_top_label'])
            body_data['y_left'] = json.dumps(body_data['y_left'])
            body_data['y_left_label'] = json.dumps(body_data['y_left_label'])
            body_data['y_right'] = json.dumps(body_data['y_right'])
            body_data['y_right_label'] = json.dumps(body_data['y_right_label'])
            del body_data['table_id']
            body_data['table'] = table
            body_data['variety'] = variety
            body_data['creator'] = request_user
            chart = VarietyChart(**body_data)
            chart.save()
            message = '创建图表成功!'
            status_code = 201
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": {}}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )


# 某品种下的图表
class VarietyChartView(View):
    def get(self, request, vid):
        machine_code = request.GET.get('mc', None)
        all_charts = request.GET.get('all', False)
        client = get_client(machine_code)
        if not client:
            charts = VarietyChart.objects.none()
        else:
            if all_charts:
                charts = VarietyChart.objects.filter(variety_id=int(vid), table__is_deleted=False)
            else:
                charts = VarietyChart.objects.filter(variety_id=int(vid), table__is_deleted=False, is_show=True)
        serializer = ChartSerializer(instance=charts, many=True)
        return HttpResponse(
            content=json.dumps({"message": '获取图表信息成功！', "data": serializer.data}),
            content_type="application/json; charset=utf-8",
            status=200
        )


# 单个图表视图
class ChartRetrieveView(View):
    def get(self, request, cid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        try:
            if not client:
                raise ValueError('INVALID CLIENT!')
            # 查询表
            chart = VarietyChart.objects.get(id=int(cid))
            serializer = ChartSerializer(instance=chart)
            data = serializer.data
            # 查询表详情的sql语句
            query_sql = "SELECT * FROM %s WHERE id>1" % chart.table.sql_name
            # 查询表头语句
            header_sql = "SELECT * FROM %s WHERE id=1" % chart.table.sql_name
            with connection.cursor() as cursor:
                cursor.execute(header_sql)
                header_data = cursor.fetchone()
                cursor.execute(query_sql)
                table_data = cursor.fetchall()  # 起始时间
                data['header_data'] = header_data
                data['table_data'] = table_data
            message = '获取表数据成功！'
            status_code = 200
        except Exception as e:
            data = {}
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": data}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )

    def patch(self, request, cid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user:
                raise ValueError('登录已过期请重新登录!')
            # 根据表获取品种
            chart = VarietyChart.objects.get(id=int(cid))
            # 修改图表
            body_data = json.loads(request.body)
            for key, value in body_data.items():
                if key in ['is_top', 'is_show']:
                    if key == 'is_top':
                        if not request_user.is_operator: # 运营管理才能设置
                            raise ValueError('您不能进行这个操作!')
                    elif key == 'is_show':
                        if not variety_user_accessed(variety=chart.variety, user=request_user):
                            raise ValueError('您不能进行这项操作!')
                    else:
                        pass
                    chart.__setattr__(key, value)
            chart.save()
            message = '展示状态修改成功!'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({'message': message, 'data': {}}),
            content_type='application/json; charset=utf-8',
            status=status_code
        )

    def delete(self, request, cid):
        machine_code = request.GET.get('mc', None)
        client = get_client(machine_code)
        request_user = request.user
        try:
            if not client or not client.is_manager:
                raise ValueError('INVALID CLIENT!')
            if not request_user:
                raise ValueError('登录已过期！')
            # 查询表
            chart = VarietyChart.objects.get(id=int(cid))
            if not variety_user_accessed(variety=chart.variety, user=request_user):
                raise ValueError('您还没有该品种的权限!不能删除。')
            chart.delete()
            message = '删除图表成功!'
            status_code = 200
        except Exception as e:
            message = str(e)
            status_code = 400
        return HttpResponse(
            content=json.dumps({"message": message, "data": {}}),
            content_type="application/json; charset=utf-8",
            status=status_code
        )







