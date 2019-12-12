# Generated by Django 2.1 on 2019-12-12 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
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
            unique_together={('group', 'name_en'), ('group', 'name')},
        ),
    ]
