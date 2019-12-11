# Generated by Django 2.1 on 2019-12-11 09:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserToClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('expire_date', models.DateTimeField(blank=True, null=True, verbose_name='失效时间')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Client', verbose_name='客户端')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户-客户端',
                'verbose_name_plural': '用户-客户端',
                'db_table': 'limit_user_client',
            },
        ),
        migrations.CreateModel(
            name='UserToModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('expire_date', models.DateTimeField(default=datetime.datetime(3000, 1, 1, 0, 0), verbose_name='失效时间')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Module', verbose_name='模块')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户-模块',
                'verbose_name_plural': '用户-模块',
                'db_table': 'limit_user_module',
            },
        ),
        migrations.AlterUniqueTogether(
            name='usertomodule',
            unique_together={('user', 'module')},
        ),
        migrations.AlterUniqueTogether(
            name='usertoclient',
            unique_together={('user', 'client')},
        ),
    ]
