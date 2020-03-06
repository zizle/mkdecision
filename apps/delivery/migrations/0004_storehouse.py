# Generated by Django 2.1 on 2020-03-05 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0003_auto_20200304_1528'),
        ('delivery', '0003_auto_20200304_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreHouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('province', models.CharField(max_length=16, verbose_name='所属省份')),
                ('name', models.CharField(max_length=64, verbose_name='名称')),
                ('house_code', models.CharField(max_length=8, unique=True, verbose_name='仓库编码')),
                ('arrived', models.CharField(max_length=512, verbose_name='到达站')),
                ('premium', models.CharField(max_length=512, verbose_name='升贴水')),
                ('address', models.CharField(max_length=512, verbose_name='地址')),
                ('link', models.CharField(max_length=256, verbose_name='联系人')),
                ('tel_phone', models.CharField(max_length=512, verbose_name='联系电话')),
                ('fax', models.CharField(max_length=64, verbose_name='传真')),
                ('longitude', models.FloatField(verbose_name='经度')),
                ('latitude', models.FloatField(verbose_name='纬度')),
                ('variety', models.ManyToManyField(to='basic.Variety', verbose_name='品种')),
            ],
            options={
                'verbose_name': '交割仓库',
                'verbose_name_plural': '交割仓库',
                'db_table': 'delivery_storehouse',
            },
        ),
    ]