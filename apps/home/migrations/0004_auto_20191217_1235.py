# Generated by Django 2.1 on 2019-12-17 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('basic', '0002_auto_20191212_1127'),
        ('home', '0003_auto_20191217_1001'),
    ]

    operations = [
        migrations.CreateModel(
            name='NormalReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=256, verbose_name='文件名')),
                ('file', models.FileField(upload_to='home/normalReport/%Y/%m/%d/')),
                ('date', models.DateField(verbose_name='报告日期')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='normal_reports', to='home.DataCategory', verbose_name='所属分类')),
                ('uploader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='report_files', to=settings.AUTH_USER_MODEL, verbose_name='上传者')),
                ('varieties', models.ManyToManyField(related_name='variety_reports', to='basic.Variety', verbose_name='所属品种')),
            ],
            options={
                'verbose_name': '常规报告',
                'verbose_name_plural': '常规报告',
                'db_table': 'home_normal_report',
            },
        ),
        migrations.AlterUniqueTogether(
            name='normalreport',
            unique_together={('name', 'date')},
        ),
    ]
