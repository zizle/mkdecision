# Generated by Django 2.1 on 2020-03-06 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0005_varietyinformation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='varietyinformation',
            name='variety',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='infos', to='basic.Variety', verbose_name='品种'),
        ),
    ]