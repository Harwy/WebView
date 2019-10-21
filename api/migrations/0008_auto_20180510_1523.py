# Generated by Django 2.0.3 on 2018-05-10 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20180506_2129'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckBox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boxTime', models.DateTimeField(auto_now_add=True)),
                ('boxCheck', models.CharField(max_length=6)),
                ('boxEmail', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='newtime', to='api.Device'),
        ),
    ]