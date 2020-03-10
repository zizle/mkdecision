# Generated by Django 2.1 on 2020-03-10 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HedgePlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=256, verbose_name='名称')),
                ('file', models.FileField(upload_to='info/hedgePlan/%Y/%m/%d/')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': '套保方案',
                'verbose_name_plural': '套保方案',
                'db_table': 'info_hedge_plan',
            },
        ),
        migrations.CreateModel(
            name='InvestPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=256, verbose_name='名称')),
                ('file', models.FileField(upload_to='info/ivtPlan/%Y/%m/%d/')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': '投资方案',
                'verbose_name_plural': '投资方案',
                'db_table': 'info_invest_plan',
            },
        ),
        migrations.CreateModel(
            name='MarketAnalysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=256, verbose_name='名称')),
                ('file', models.FileField(upload_to='info/marketAly/%Y/%m/%d/')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': '市场分析',
                'verbose_name_plural': '市场分析',
                'db_table': 'info_market_analysis',
            },
        ),
        migrations.CreateModel(
            name='MessageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('date', models.DateField(verbose_name='日期')),
                ('time', models.TimeField(verbose_name='时间')),
                ('content', models.CharField(max_length=2048, verbose_name='内容')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': '短信通',
                'verbose_name_plural': '短信通',
                'db_table': 'info_message_link',
            },
        ),
        migrations.CreateModel(
            name='SearchReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=256, verbose_name='名称')),
                ('file', models.FileField(upload_to='info/searchRpt/%Y/%m/%d/')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': '调研报告',
                'verbose_name_plural': '调研报告',
                'db_table': 'info_search_report',
            },
        ),
        migrations.CreateModel(
            name='TopicSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=256, verbose_name='名称')),
                ('file', models.FileField(upload_to='info/topicSch/%Y/%m/%d/')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': '调研报告',
                'verbose_name_plural': '调研报告',
                'db_table': 'info_topic_search',
            },
        ),
        migrations.CreateModel(
            name='TradePolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('date', models.DateField(verbose_name='日期')),
                ('time', models.TimeField(verbose_name='时间')),
                ('content', models.CharField(max_length=2048, verbose_name='内容')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': '交易策略',
                'verbose_name_plural': '交易策略',
                'db_table': 'info_trade_policy',
            },
        ),
    ]
