# Generated by Django 2.0.3 on 2018-04-29 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180428_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Device'),
        ),
    ]