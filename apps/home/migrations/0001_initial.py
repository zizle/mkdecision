# Generated by Django 2.1 on 2020-03-13 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('basic', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=64, verbose_name='标题')),
                ('image', models.FileField(upload_to='home/advertisement/image/', verbose_name='图片')),
                ('file', models.FileField(blank=True, upload_to='home/advertisement/', verbose_name='文件')),
                ('content', models.TextField(blank=True, verbose_name='内容')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': '首页广告',
                'verbose_name_plural': '首页广告',
                'db_table': 'home_advertisement',
            },
        ),
        migrations.CreateModel(
            name='DataCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=16, verbose_name='名称')),
                ('group', models.CharField(choices=[('normal_report', '常规报告'), ('transaction_notice', '交易通知')], max_length=32, verbose_name='组别')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
                'db_table': 'home_data_category',
            },
        ),
        migrations.CreateModel(
            name='FinanceCalendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('date', models.DateField(verbose_name='日期')),
                ('time', models.TimeField(verbose_name='时间')),
                ('country', models.CharField(max_length=128, verbose_name='地区')),
                ('event', models.TextField(verbose_name='事件')),
                ('expected', models.CharField(max_length=64, verbose_name='预期值')),
                ('uploader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='上传者')),
            ],
            options={
                'verbose_name': '财经日历',
                'db_table': 'home_finance_calendar',
            },
        ),
        migrations.CreateModel(
            name='NewsBulletin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('file', models.FileField(blank=True, upload_to='home/news/%Y/%m/%d/', verbose_name='文件')),
                ('content', models.TextField(blank=True, verbose_name='内容')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
            ],
            options={
                'verbose_name': '新闻公告',
                'verbose_name_plural': '新闻公告',
                'db_table': 'home_news',
            },
        ),
        migrations.CreateModel(
            name='NormalReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=256, verbose_name='文件名')),
                ('file', models.FileField(upload_to='home/normalReport/%Y/%m/%d/')),
                ('date', models.DateField(verbose_name='报告日期')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='normal_reports', to='home.DataCategory', verbose_name='所属分类')),
                ('uploader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='report_files', to=settings.AUTH_USER_MODEL, verbose_name='上传者')),
                ('varieties', models.ManyToManyField(related_name='variety_reports', to='basic.Variety', verbose_name='所属品种')),
            ],
            options={
                'verbose_name': '常规报告',
                'verbose_name_plural': '常规报告',
                'db_table': 'home_normal_report',
            },
        ),
        migrations.CreateModel(
            name='SpotCommodity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('area', models.CharField(max_length=128, verbose_name='地区')),
                ('level', models.CharField(max_length=16, verbose_name='等级')),
                ('price', models.FloatField(verbose_name='价格')),
                ('increase', models.FloatField(verbose_name='增减')),
                ('date', models.DateField(verbose_name='日期')),
                ('note', models.CharField(blank=True, max_length=256, null=True, verbose_name='备注')),
                ('uploader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='上传者')),
            ],
            options={
                'verbose_name': '现货报表',
                'db_table': 'home_spot_commodity',
            },
        ),
        migrations.CreateModel(
            name='TransactionNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=256, verbose_name='文件名')),
                ('file', models.FileField(upload_to='home/transactionNotice/%Y/%m/%d/')),
                ('date', models.DateField(verbose_name='通知日期')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_notice', to='home.DataCategory', verbose_name='所属分类')),
                ('uploader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notice_files', to=settings.AUTH_USER_MODEL, verbose_name='上传者')),
            ],
            options={
                'verbose_name': '交易通知',
                'verbose_name_plural': '交易通知',
                'db_table': 'home_transaction_notice',
            },
        ),
        migrations.AlterUniqueTogether(
            name='datacategory',
            unique_together={('name', 'group')},
        ),
        migrations.AlterUniqueTogether(
            name='transactionnotice',
            unique_together={('name', 'date')},
        ),
        migrations.AlterUniqueTogether(
            name='spotcommodity',
            unique_together={('name', 'date')},
        ),
        migrations.AlterUniqueTogether(
            name='normalreport',
            unique_together={('name', 'date')},
        ),
    ]
