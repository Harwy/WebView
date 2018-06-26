# Generated by Django 2.0.3 on 2018-05-18 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20180510_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('control', models.CharField(default='0', max_length=2)),
                ('isDo', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='command',
            name='device_command',
            field=models.ForeignKey(default=5, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deviceCommand', to='api.Device'),
        ),
        migrations.AlterField(
            model_name='device',
            name='devTag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.ProUser'),
        ),
        migrations.AlterField(
            model_name='product',
            name='message',
            field=models.CharField(default='normal', max_length=100),
        ),
        migrations.AddField(
            model_name='control',
            name='device_control',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deviceControl', to='api.Device'),
        ),
    ]
