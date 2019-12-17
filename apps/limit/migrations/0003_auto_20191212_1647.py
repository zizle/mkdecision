# Generated by Django 2.1 on 2019-12-12 16:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0002_auto_20191212_1127'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('limit', '0002_auto_20191211_1024'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserToVariety',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('expire_date', models.DateField(default=datetime.datetime(3000, 1, 1, 0, 0), verbose_name='失效时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
                ('variety', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Variety', verbose_name='品种')),
            ],
            options={
                'verbose_name': '用户-品种',
                'verbose_name_plural': '用户-品种',
                'db_table': 'limit_user_variety',
            },
        ),
        migrations.AlterUniqueTogether(
            name='usertovariety',
            unique_together={('user', 'variety')},
        ),
    ]