# Generated by Django 2.0.3 on 2018-05-01 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20180429_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='prouser',
            name='userLogin',
            field=models.BooleanField(default=False),
        ),
    ]
