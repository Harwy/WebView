from rest_framework import serializers
from api.models import Product , Command, Test, ProUser, Device, Control


class ProUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProUser
        fields = ('id', 'userName', 'userAge', 'userSex',  'userEmail', 'userAddress')


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProUser
        fields = ('id', 'userName')


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'devName', 'devTag', 'devId')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'created', 'message','temp', 'hum' , 'pm2_5', 'hcho', 'device', 'isDelete')


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'created','temp', 'hum' , 'pm2_5', 'hcho', 'device')


'''
    设备列表，包括当前最新的数据（一条）
'''
class DeviceListSerializer(serializers.ModelSerializer):
    # product = Product.objects.order_by('-created')[0]
    newtime = ProductListSerializer


    class Meta:
        model = Device
        fields = ('id', 'devName', 'devTag', 'devId', 'newtime')





class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ('id', 'command', 'isDo')


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('id', 'testTime', 'testMessage')



