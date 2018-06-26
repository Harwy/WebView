from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import django.utils.timezone as timezone

from django.utils.html import format_html


# Create your models here.数据库模型，三个参数，创建时间 and 接收的消息 and 是否删除
class ProUser(models.Model):
    userName = models.CharField(u'用户名',max_length=8)
    userPassword = models.CharField(u'密码', max_length=120, default=make_password('123456', None, 'pbkdf2_sha256'))
    userAge = models.CharField(u'年龄',max_length=3,default='10')
    sex = (
        (1,'男'),
        (2,'女'),
        )
    userSex = models.IntegerField(u'性别',choices=sex, default=1) # 性别
    userEmail = models.EmailField(u'邮箱',max_length=100, default='default@django.com')
    userAddress = models.CharField(u'地址',max_length=50, default='')
    userCity = models.CharField(u'城市',max_length=60, default='')
    userStateProvince = models.CharField(u'省份',max_length=30, default='')
    userCountry = models.CharField(u'国家',max_length=50, default='')
    userLogin = models.BooleanField(u'登录状态',default=False)


    def __str__(self):  # 返回类型
        return self.userName

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"


# 设备详情
class Device(models.Model):
    devName = models.CharField(u'设备名',max_length=100, default='')
    devId = models.CharField(u'设备ID',max_length=10 , default='12345')
    devTag = models.ForeignKey(ProUser, null=True, on_delete=models.CASCADE,verbose_name='关联用户')
    def __str__(self):  # 返回类型
        return self.devName
    class Meta:
        verbose_name = "设备"
        verbose_name_plural = "设备"



# 设备数据
class Product(models.Model):
    created = models.DateTimeField(u'更新时间', auto_now_add=True)  # default = timezone.now
    message = models.CharField(u'设备IP',max_length=100, default='normal')
    hum = models.FloatField(u'湿度',default=0)  # 温度
    temp = models.FloatField(u'温度',default=0)  # 湿度
    pm2_5 = models.FloatField(u'PM2.5',default=0)  # pm2.5
    hcho = models.FloatField(u'甲醛浓度',default=0)  # 甲醛
    device = models.ForeignKey(Device, related_name="newtime",null=True, on_delete=models.CASCADE,verbose_name='关联设备')  # 设备号
    isDelete = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = "设备数据"
        verbose_name_plural = "设备数据"

    def __unicode__(self):
        return '%s: %s: %s: %s: %s' % (self.created, self.hum, self.temp, self.pm2_5, self.hcho)



# 通知指令表
class Command(models.Model):
    device_command = models.ForeignKey(Device, related_name="deviceCommand", null=True, on_delete=models.CASCADE, default=5,verbose_name='关联设备')
    command_list = (
        (0, '空指令'),
        (1, '温度过高警报'),
        (2, '湿度过高警报'),
        (3, 'PM2.5过高警报'),
        (4, '甲醛过高警报'),
    )
    command = models.IntegerField(u'通知指令',choices=command_list, default=0)  # 指令传递编号
    isDo = models.BooleanField(default=True)  # 指令，默认已经执行，下位机不处理

    class Meta:
        verbose_name = "通知指令"
        verbose_name_plural = "通知指令"

# 控制指令表
class Control(models.Model):
    device_control = models.ForeignKey(Device, related_name="deviceControl", null=True, on_delete=models.CASCADE, default=5,verbose_name='关联设备')
    control_list = (
        (0, '空指令'),
        (1, '打开灯'),
        (2, '关上灯'),
        (3, '打开设备'),
        (4, '关闭设备'),
        )
    control = models.IntegerField(u'控制指令',choices=control_list, default=0)  #控制命令编号
    isDo = models.BooleanField(default=True) # 指令，默认已经执行，下位机不处理

    class Meta:
        verbose_name = "控制指令"
        verbose_name_plural = "控制指令"





class Test(models.Model):
    testTime = models.DateTimeField(auto_now_add=True)
    testMessage = models.CharField(max_length=100, default='')

    class Meta:
        verbose_name = "测试用数据集"
        verbose_name_plural = "测试用数据集"


class CheckBox(models.Model):
    boxTime = models.DateTimeField(auto_now_add=True)
    boxCheck = models.CharField(max_length=6, default='000000')
    boxEmail = models.EmailField(default='default@django.com')
    modes = (
        (1, '注册'),
        (2, '重置密码'),
        (3, '其实没什么用'),
    )
    boxMode = models.IntegerField(choices=modes, default=3)

    class Meta:
        verbose_name = "注册验证"
        verbose_name_plural = "注册验证"

