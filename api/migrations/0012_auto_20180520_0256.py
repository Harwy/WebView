# Generated by Django 2.0.3 on 2018-05-20 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20180518_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='control',
            name='control',
            field=models.IntegerField(choices=[(0, '空指令'), (1, '打开灯'), (2, '关上灯'), (3, '打开设备'), (4, '关闭设备')], default=0),
        ),
    ]
