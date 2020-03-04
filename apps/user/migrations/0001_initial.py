# Generated by Django 2.1 on 2020-02-28 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(blank=True, max_length=20, verbose_name='用户名/昵称')),
                ('phone', models.CharField(max_length=11, unique=True, verbose_name='手机')),
                ('avatar', models.CharField(default='', max_length=512, verbose_name='头像')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='邮箱')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('note', models.CharField(blank=True, max_length=20, null=True, verbose_name='备注')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='超级管理员')),
                ('is_operator', models.BooleanField(default=False, verbose_name='运营管理员')),
                ('is_collector', models.BooleanField(default=False, verbose_name='信息管理员')),
                ('is_researcher', models.BooleanField(default=False, verbose_name='品种研究员')),
                ('is_active', models.BooleanField(default=True, verbose_name='有效用户')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'user_user',
            },
        ),
    ]
