# Generated by Django 2.0.3 on 2018-05-10 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20180510_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkbox',
            name='boxMode',
            field=models.IntegerField(choices=[(1, '注册'), (2, '重置密码'), (3, '其实没什么用')], default=3),
        ),
        migrations.AlterField(
            model_name='checkbox',
            name='boxCheck',
            field=models.CharField(default='000000', max_length=6),
        ),
        migrations.AlterField(
            model_name='checkbox',
            name='boxEmail',
            field=models.EmailField(default='default@django.com', max_length=254),
        ),
    ]
