# Generated by Django 2.1 on 2019-12-27 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info_service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infoservice',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='info_service.InfoGroup', verbose_name='服务内容'),
        ),
    ]
