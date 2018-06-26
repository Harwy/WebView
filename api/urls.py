from django.conf.urls import url
from . import views as views_api

from rest_framework.routers import DefaultRouter
from api.views import ProductViewSet , CommandViewSet, TestViewSet, ProUserViewSet, DeviceViewSet
from django.urls import path, include

"""
      39.106.213.217:8080/api/prouser/
      GET：获取所有用户信息
      POST：添加一名用户信息
      PATCH：修改一个信息
      39.106.213.217:8080/api/prouser/<pk>
      根据用户编号返回用户信息
      ===================================
      39.106.213.217:8080/api/device/
      39.106.213.217:8080/api/device/<pk>
      39.106.213.217:8080/api/product/
      39.106.213.217:8080/api/product/<pk>
      39.106.213.217:8080/api/login/  login  实现登录
      39.106.213.217:8080/api/signin/  注册
      39.106.213.217:8080/api/edit_user/ 完善个人信息
      39.106.213.217:8080/api/edit_device/  创建设备
      39.106.213.217:8080/api/get_new_device/   根据用户返回设备列表
      39.106.213.217:8080/api/get_new_data/    根据设备返回设备最新一条数据
      39.106.213.217:8080/api/get_user/  返回所有用户名
      
      
      
"""

router = DefaultRouter()
router.register(r'prouser', ProUserViewSet, )
router.register(r'device', DeviceViewSet,)
router.register(r'product', ProductViewSet,)
router.register(r'command', CommandViewSet,)
router.register(r'test', TestViewSet,)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/', views_api.login),  # 39.106.213.217:8080/api/login/  username="root" password="123456"    返回'msg'
    url(r'^signin/', views_api.signin),
    url(r'^edit_user/', views_api.edit_user),
    url(r'^edit_device/', views_api.edit_device),
    url(r'^mailcheck/', views_api.mail_check),
    url(r'^notice/', views_api.command_get),  # app后台通知

    #""" ------控制硬件指令队列------  """
    url(r'^control/(?P<id>\w+)/get/', views_api.control_get, name="control"),
    url(r'^control/(?P<id>\w+)/(?P<control>\w+)/push/', views_api.control_push, name="control"),

    # 上位机上传数据（更新版api）
    url(r'^products/add/', views_api.add_product, name="products"),

    url(r'^connect/(?P<deviceid>\w+)/(?P<userid>\w+)/', views_api.user_connect_device, name="device"),

    # url(r'^get_new_data/', views_api.get_new_data),
    # url(r'^get_new_device/', views_api.get_new_device),
    # url(r'^get_user/', views_api.get_user),
    url(r'^search/(?P<name>\w+)/', views_api.search_data_by_year_month, name="search_name")
    # url(r'^test/$', views_api.GetMessageView.as_view()),
]
