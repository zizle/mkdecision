# Generated by Django 2.1 on 2020-02-28 09:33

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
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='名称备注')),
                ('machine_code', models.CharField(max_length=32, unique=True, verbose_name='机器识别码')),
                ('is_manager', models.BooleanField(default=False, verbose_name='管理端')),
                ('is_active', models.BooleanField(default=True, verbose_name='有效')),
            ],
            options={
                'verbose_name': '客户端',
                'verbose_name_plural': '客户端',
                'db_table': 'basic_client',
            },
        ),
        migrations.CreateModel(
            name='ClientOpenRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Client', verbose_name='客户端')),
            ],
            options={
                'verbose_name': '客户端打开记录',
                'verbose_name_plural': '客户端打开记录',
                'db_table': 'basic_client_opened',
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='名称')),
                ('order', models.IntegerField(default=0, verbose_name='排序')),
                ('is_active', models.BooleanField(default=True, verbose_name='启用')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_modules', to='basic.Module', verbose_name='父级')),
            ],
            options={
                'verbose_name': '主功能菜单',
                'verbose_name_plural': '主功能菜单',
                'db_table': 'basic_module',
            },
        ),
        migrations.CreateModel(
            name='ModuleOpenRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Client', verbose_name='客户端')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Module', verbose_name='模块')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '模块访问记录',
                'verbose_name_plural': '模块访问记录',
                'db_table': 'basic_module_opened',
            },
        ),
        migrations.CreateModel(
            name='Variety',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=16, verbose_name='名称')),
                ('name_en', models.CharField(max_length=32, verbose_name='名称')),
            ],
            options={
                'verbose_name': '品种',
                'verbose_name_plural': '品种',
                'db_table': 'basic_variety',
            },
        ),
        migrations.CreateModel(
            name='VarietyGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='组名')),
            ],
            options={
                'verbose_name': '品种组别',
                'verbose_name_plural': '品种组别',
                'db_table': 'basic_variety_group',
            },
        ),
        migrations.AddField(
            model_name='variety',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='varieties', to='basic.VarietyGroup', verbose_name='所属组'),
        ),
        migrations.AlterUniqueTogether(
            name='variety',
            unique_together={('group', 'name'), ('group', 'name_en')},
        ),
    ]
