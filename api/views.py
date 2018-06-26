from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from django.core import serializers

from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import detail_route, list_route, action
from api.serializers import ProductSerializer, CommandSerializer, TestSerializer, ProUserSerializer, DeviceSerializer, UserAdminSerializer, DeviceListSerializer, ProductListSerializer
from api.models import Product, Command, Test, ProUser, Device, CheckBox, Control
from mail.views import SendEmail

# 加密
from django.contrib.auth.hashers import make_password, check_password

# 邮箱部分
import random

import json
import datetime


# Create your views here.
class GetMessageView(APIView):
    # get 请求
    def get(self, request):
        # 获取参数数据
        get = request.GET
        # 获取参数 a
        a = get.get('a')
        print(a)
        # 返回信息
        d = {
            'status': 1,
            'message': 'success',
            }
        return JsonResponse(d)





# 验证码   mailcheck/
@csrf_exempt
def mail_check(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    if request.method == 'POST':
        # 解析请求的json格式入参
        data = JSONParser().parse(request)
        check_email = data['email']
        mode = data['mode']
        check = random.randint(100000, 999999)
        # 验证该邮箱是否注册过
        try:
            admin = ProUser.objects.get(userEmail=check_email)
        except ProUser.DoesNotExist:
            if mode == "1":  # 注册邮箱验证码
                # 可以注册
                content = {'msg': '1', 'mode': '1'}
                body = "欢迎注册KEEP HOME\n" + "这是你的验证码：" + str(check) + "\n30分钟内有效"
                SendEmail.send_text_email("KEEP HOME 验证码", "KEEP HOME 验证码", body, [check_email])
                a = CheckBox(boxCheck=str(check), boxEmail=check_email, boxMode=1)
                a.save()
            else:   # 忘记密码验证码
                content = {'msg': '2', 'mode': '2'}
        else:
            # 用户存在，不可注册，可忘记密码操作
            if mode == "1":
                content = {'msg': '2', 'mode': '1'}
            else:
                content = {'msg': '1', 'mode': '2'}
                body = "KEEP HOME帮助你重置忘记的密码哦\n" + "这是你的验证码：" + str(check) + "\n30分钟内有效"
                SendEmail.send_text_email( "KEEP HOME 验证码", "KEEP HOME 验证码", body, [check_email])
                a = CheckBox(boxCheck=str(check), boxEmail=check_email, boxMode=2)
                a.save()
        print("结果为：",content)
        return JsonResponse(data=content, status=status.HTTP_200_OK)

""""
---------------------------
    实现登录(使用系统默认用户)
---------------------------
"""
@csrf_exempt
def login_admin(request):
    pass

# 解析请求的json格式入参

""""
---------------------------
    实现登录(功能实现)
---------------------------
"""
@csrf_exempt
def login(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    if request.method == 'POST':
        # 解析请求的json格式入参
        data = JSONParser().parse(request)
        username = data['username']
        password = data['password']
        try:
            admin = ProUser.objects.get(userName=username)
        except ProUser.DoesNotExist:
            content = {'msg':'1', 'id':'0'}
            return JsonResponse(data=content, status=status.HTTP_200_OK)
        else:
            if check_password(password, admin.userPassword):
                admin.userLogin = True
                admin.save()
                content = {'msg': '0', 'id': str(admin.id)}
                return JsonResponse(data=content, status=status.HTTP_200_OK)
            else:
                content = {'msg': '2', 'id': '0'}
                return JsonResponse(data=content, status=status.HTTP_200_OK)


"""
-----------------------
    注册
-----------------------
"""
@csrf_exempt
def signin(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    if request.method == 'POST':
        # 解析请求的json格式入参
        data = JSONParser().parse(request)
        username = data['name']
        password = data['password']
        email = data['email']
        check = data['check']
        checkModel = CheckBox.objects.last()
        if checkModel != None:
            if check == checkModel.boxCheck:
                try:
                    admin = ProUser.objects.get(userName=username)  # 查询账号是否存在
                except ProUser.DoesNotExist:
                    # 完成注册
                    ProUser.objects.create(userName=username, userPassword=make_password(password, None, 'pbkdf2_sha256'), userEmail=email)
                    checkModel.delete()
                    content = {'sign': '0', 'mode': '0'}
                else:
                    content = {'sign': '1', 'mode': '0'}  # sign==1 账号已存在，不能注册
            else:
                content = {'sign': '2', 'mode': '0'}  # sign==2 验证码错误，不能注册
        else:
            content = {'sign': '3', 'mode': '0'}  # sign==3 验证码不存在，不能注册
        print("注册结果：",content)
        return JsonResponse(data=content, status=status.HTTP_200_OK)



"""
    完善个人信息(实现)
"""
@csrf_exempt
def edit_user(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    if request.method == 'POST':
        # 解析请求的json格式入参
        data = JSONParser().parse(request)
        username = data['userName']
        age = data['userAge']
        sex = data['userSex']
        email = data['userEmail']
        address = data['userAddress']
        try:
            admin = ProUser.objects.get(userName=username)  # 查询账号是否存在
        except ProUser.DoesNotExist:
            content = {'edit': '1'}
            return JsonResponse(data=content, status=status.HTTP_200_OK)
        else:
            admin.userAge = age
            admin.userSex = sex
            admin.userEmail = email
            admin.userAddress = address
            admin.save()
            content = {'edit': '0'}
            return JsonResponse(data=content, status=status.HTTP_200_OK)

"""
    创建设备
    功能：设备名，绑定用户
"""
@csrf_exempt
def edit_device(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        name = data['device']
        username = data['username']
        try:
            device = Device.objects.get(devName=name)  # 查询设备名是否存在
        except Device.DoesNotExist:
            device.devName = name
            device.save()
            content = {'edit_dev': '1'}  # 没有该设备,创建该设备
            return JsonResponse(data=content, status=status.HTTP_200_OK)
        else:
            admin = ProUser.objects.get(userName=username)  # 查询账号是否存在
            device.devTag = admin
            device.save()
            content = {'edit_dev': '0'}
            return JsonResponse(data=content, status=status.HTTP_200_OK)



"""
----------------------------------
    根据设备返回设备最新一条数据
    参数：设备名称
----------------------------------
"""
@csrf_exempt
def get_new_data(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    if request.method == 'POST':
        data = JSONParser().parse(request)
        device = data['device']
        tag = Device.objects.get(devName=device)
        p = Product.objects.filter(device=tag).order_by('-created')[0]
        content = {}
        content['id'] = p.id
        content['created'] = p.created
        content['hum'] = p.hum
        content['temp'] = p.temp
        content['hcho'] = p.hcho
        content['pm2_5'] = p.pm2_5
        return JsonResponse(data=content, status=status.HTTP_200_OK, safe=False)



class ProUserViewSet(viewsets.ModelViewSet):
    queryset = ProUser.objects.all()
    serializer_class = ProUserSerializer # UserAdminSerializer

    # 根据用户id返回该用户下所有设备id
    @action(methods=['GET'], detail=True, url_path='device', url_name='device')
    def searchDevList(self, request, pk=None):
        devices = Device.objects.filter(devTag=pk)
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

    """
        实现用户到设备列表查找（功能完成）
    """
    @action(methods=['GET'], detail=True, url_path='product', url_name='product')
    def searchProduct(self, request, pk=None):
        devices = Device.objects.filter(devTag=pk)
        add = []
        q = Product.objects.all()
        for d in devices:
            p = q.filter(device=d.id).order_by('-created')[0]
            content = {}
            t = {}
            t['created'] = p.created
            t['message'] = p.message
            t['hum'] = p.hum
            t['temp'] = p.temp
            t['pm2_5'] = p.pm2_5
            t['hcho'] = p.hcho
            content['nowtime'] = t
            content['id'] = d.id
            content['devName'] = d.devName
            content['devId'] = d.devId
            add.append(content)
        return JsonResponse(data= add, status=status.HTTP_200_OK, safe=False)


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    # 根据设备id返回所有数据(30条)
    @action(methods=['GET'],detail=True,url_path='search', url_name='search')
    def searchDev(self, request, pk=None):
        devices = Device.objects.get(pk=pk)
        add = []
        p = Product.objects.filter(device=devices.pk).order_by('-created')[:30]
        content = {}
        for d in p:
            t = {}
            t['created'] = d.created
            t['hum'] = d.hum
            t['temp'] = d.temp
            t['pm2_5'] = d.pm2_5
            t['hcho'] = d.hcho
            add.append(t)
        content['nowtime'] = add
        content['id'] = devices.id
        content['devName'] = devices.devName
        content['devId'] = devices.devId

        return JsonResponse(data= content, status=status.HTTP_200_OK, safe=False)

    # 根据设备id返回最新一条数据
    @action(methods=['GET'], detail=True, url_path='search1', url_name='search1')
    def searchDev_1(self, request, pk=None):
        product = Product.objects.filter(device=pk).order_by('created')[0]
        serializer = ProductListSerializer(product)
        return Response(serializer.data)

    # 根据设备id返回7天数据
    @action(methods=['GET'], detail=True, url_path='sevenday', url_name='seven_day')
    def back_seven_day_product(self, request, pk=None):
        devices = Device.objects.get(pk=pk)
        add = []
        content = {}
        """获取7天内的数据"""
        # 得到7天的日期
        now = datetime.datetime.now()
        end_date = datetime.datetime(now.year, now.month, now.day, 0, 0)
        start_date = end_date - datetime.timedelta(7)
        days = map(lambda x: end_date - datetime.timedelta(x), range(7, 0, -1))

        # 得到前7天的环境数据
        oneday = datetime.timedelta(1)
        # counts_temp = map(lambda x: Product.objects.filter(device=pk, created__range=(x,x + oneday)), days)
        for x in days:
            t = {}
            product = Product.objects.filter(device=pk)
            product_count = product.filter(created__range=(x,x + oneday))
            temp_count = 0
            hum_count = 0
            pm2_5_count = 0
            hcho_count = 0
            for d in product_count:
                temp_count += d.temp
                hum_count += d.hum
                pm2_5_count += d.pm2_5
                hcho_count += d.hcho
            if product_count.count() != 0:
                t['temp'] = 1.0 * temp_count / product_count.count()
                t['hum'] = 1.0 * hum_count / product_count.count()
                t['pm2_5'] = 1.0 * pm2_5_count / product_count.count()
                t['hcho'] = 1.0 * hcho_count / product_count.count()
                t['temp'] = round(t['temp'], 1)
                t['hum'] = round(t['hum'], 1)
                t['pm2_5'] = round(t['pm2_5'], 1)
                t['hcho'] = round(t['hcho'], 1)
            else:
                t['temp'] = 0
                t['hum'] = 0
                t['pm2_5'] = 0
                t['hcho'] = 0
            # t['created'] = str(x)[5:10]
            t['created'] = str(x)[5:10]
            # print(t['created'])
            add.append(t)
            # print(add)
        # 汇总JSON
        p = product.order_by('-created')[0]
        t = {}
        t['temp'] = p.temp
        t['hum'] = p.hum
        t['pm2_5'] = p.pm2_5
        t['hcho'] = p.hcho
        t['created'] = str(p.created)
        add.append(t)
        content['nowtime'] = add
        content['id'] = devices.id
        content['devName'] = devices.devName
        content['devId'] = devices.devId
        return JsonResponse(data=content, status=status.HTTP_200_OK, safe=False)

"""
---------------------------------
    根据设备id与对应用户id绑定
---------------------------------
"""
@csrf_exempt
def user_connect_device(request, deviceid, userid):
    if request.method == 'GET':
        try:
            device = Device.objects.get(pk=deviceid)
        except Device.DoesNotExist:
            content = { 'state': 0 }
        else:
            device.devTag = ProUser.objects.get(pk=userid)
            device.save()
            content = { 'state': 1 }
        return JsonResponse(data=content, status=status.HTTP_200_OK)







class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # 根据设备号返回一条最新数据
    @action(methods=['GET'], detail=True, url_path='onedata', url_name='onedata')
    def get1data(self, request, pk=None):
        product = Product.objects.filter(device_id=pk).order_by('-created')[0]
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @list_route()
    def filterProducts(self, request):
        products = Product.objects.filter(id__in=range(3))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # # 根据年月设备号返回数据
    # @action(methods=['GET'], detail=True, url_path='manydata', url_name='manydata')
    # def getdata(self,request, pk=None, year=None, month=None):
    #     products = Product.objects.filter(device_id=pk, pub_date__year=year, pub_date__month=month).order_by('-created')
    #     serializer = ProductSerializer(products)
    #     return Response(serializer.data)

# @action(methods=['GET'], detail=True, url_path='search/(?P<year>\d{4})/(?P<month>\d{2})/(?P<pk>[0-9]+)', url_name='manydata')
@csrf_exempt
def search_data_by_year_month(request, name):
    if request.method == 'GET':
        user = ProUser.objects.get(userName=name)
        content = {}
        content['username'] = user.userName
        content['useremail'] = user.userEmail
    return JsonResponse(data=content, status=status.HTTP_200_OK, safe=False)


"""
-------------------------
    上位机传输数据
-------------------------
"""
@csrf_exempt
def add_product(request):
    # 判断请求头是否为json
    if request.content_type != 'application/json':
        # 如果不是的话，返回405
        return HttpResponse('only support json data', status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    if request.method == 'POST':
        data = JSONParser().parse(request)  # JSON解析
        temp = int(data['temp'])
        hum = int(data['hum'])
        hcho = int(data['hcho'])
        pm2_5 = int(data['pm2_5'])
        user = data['user']  # 设备用户id
        device = data['device']          # 设备id
        message = data['message']
        # 判定该设备号是否存在
        if(temp < 100 and hum <= 100 and hcho < 1000 and pm2_5 < 500): # 数据合理下进行存储
            try:
                device_list = Device.objects.get(devTag__id=user, id=device)  # 查询设备名是否存在
            except Device.DoesNotExist:
                device_list1 = Device.objects.get(id=1)  # 若设备不存在，储存在测试设备上
                Product.objects.create(temp=temp, hum=hum, hcho=hcho, pm2_5=pm2_5, message=message, device=device_list1)
                # content = {'state': 1, 'device': device_list1.devId}
                content = {'state': 1, 'device': 1}
            else:
                Product.objects.create(temp=temp, hum=hum, hcho=hcho, pm2_5=pm2_5, message=message, device=device_list)
                content = {'state': 1, 'device': user}
        else:
            content = {'state':0, 'device':user}
        return JsonResponse(data=content, status=status.HTTP_200_OK)




"""
----------------------------------
    通知任务队列
    admin下的device下的new command
----------------------------------
"""
@csrf_exempt
def command_get(request):
    if request.method == 'GET':
        content = {}
        command = Command.objects.last()
        if(command != None):
            content['state'] = 1
            content['command'] = str(command.command)
            command.delete()
        else:
            content['state'] = 0
            content['command'] = "0"
        return JsonResponse(data=content, status=status.HTTP_200_OK, safe=False)


"""
---------------------------------
控制硬件指令队列-----硬件设备获取底层指令
state = 1 ok
state = 0 error
---------------------------------
"""
@csrf_exempt
def control_get(request, id):
    if request.method == 'GET':
        content = {}
        control_item = Control.objects.filter(device_control__id=id).first()
        if(control_item != None):   # 存在指令
            content['state'] = 1
            content['control'] = control_item.control
            control_item.delete()
        else:                       # 指令队列为空
            content['state'] = 0
            content['control'] = 0
        return JsonResponse(data=content, status=status.HTTP_200_OK, safe=False)


"""
---------------------------------
控制硬件指令队列-----APP添加最新指令
state = 1 ok
state = 0 error
---------------------------------
"""
@csrf_exempt
def control_push(request, id, control):
    if request.method == 'GET':
        content = {}
        control_item = Control.objects.filter(device_control__devTag=id, control=control).first()
        if(control_item != None):       # 该指令近期已添加
            content['state'] = 0
            content['control'] = "任务已在队列中"
        else:                           # 该指令为新指令
            Control.objects.create(control=control, device_control_id=id)
            content['state'] = 1
            content['control'] = "任务设置完毕"
        return JsonResponse(data=content, status=status.HTTP_200_OK, safe=False)



class CommandViewSet(viewsets.ModelViewSet):
    queryset = Command.objects.all()
    serializer_class = CommandSerializer




class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer