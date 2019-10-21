# Generated by Django 2.0.3 on 2018-04-28 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='dev_name',
            new_name='devName',
        ),
        migrations.RenameField(
            model_name='device',
            old_name='dev_tag',
            new_name='devTag',
        ),
        migrations.RenameField(
            model_name='prouser',
            old_name='user_address',
            new_name='userAddress',
        ),
        migrations.RenameField(
            model_name='prouser',
            old_name='user_age',
            new_name='userAge',
        ),
        migrations.RenameField(
            model_name='prouser',
            old_name='user_city',
            new_name='userCity',
        ),
        migrations.RenameField(
            model_name='prouser',
            old_name='user_country',
            new_name='userCountry',
        ),
        migrations.RenameField(
            model_name='prouser',
            old_name='user_name',
            new_name='userName',
        ),
        migrations.RenameField(
            model_name='prouser',
            old_name='user_sex',
            new_name='userSex',
        ),
        migrations.RenameField(
            model_name='prouser',
            old_name='user_state_province',
            new_name='userStateProvince',
        ),
        migrations.RemoveField(
            model_name='prouser',
            name='user_email',
        ),
        migrations.AddField(
            model_name='prouser',
            name='userEmail',
            field=models.EmailField(default='default@django.com', max_length=100),
        ),
        migrations.AddField(
            model_name='prouser',
            name='userPassword',
            field=models.CharField(default='123456', max_length=20),
        ),
    ]