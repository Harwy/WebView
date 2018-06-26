from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Product , Command, ProUser, Device, CheckBox, Control


# Register your models here.
class Pm2_5ListFilter(admin.SimpleListFilter):
    title = _(u'PM2.5')
    parameter_name = 'pm2_5'

    def lookups(self, request, model_admin):
        return (
            ('0', _(u'优')),
            ('1', _(u'良')),
            ('2', _(u'轻度')),
            ('3', _(u'中度')),
            ('4', _(u'重度')),
            ('5', _(u'严重')),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(pm2_5__lt = '50')
        if self.value() == '1':
            return queryset.filter(pm2_5__gte = '50', pm2_5__lte= '100')
        if self.value() == '2':
            return queryset.filter(pm2_5__gte = '100', pm2_5__lte= '150')
        if self.value() == '3':
            return queryset.filter(pm2_5__gte = '150', pm2_5__lte= '200')
        if self.value() == '4':
            return queryset.filter(pm2_5__gte = '200', pm2_5__lte= '300')
        if self.value() == '5':
            return queryset.filter(pm2_5__gt = '300')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'hum', 'temp', 'pm2_5', 'hcho','device','created','isDelete')
    list_filter = ['created', 'device', Pm2_5ListFilter, 'message']
    search_fields = ['device', 'device', 'message']
    date_hierarchy = 'created'  # 详细时间分层筛选
    # fk_fields 设置显示外键字段
    fk_fields = ('device',)
    list_display_links = ('id', 'message')
    # 操作项功能显示位置设置，两个都为True则顶部和底部都显示
    actions_on_top =True
    actions_on_bottom = True

@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ('id', 'command', 'device_command', 'isDo')


@admin.register(ProUser)
class ProUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'userName', 'userSex','userEmail', 'userAddress')
    list_display_links = ('id', 'userName')
    list_editable = ['userSex', 'userEmail', 'userAddress']


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'devName', 'devTag')
    list_filter = ['devTag']
    list_display_links = ('devName',)
    list_editable = ['devTag']

@admin.register(CheckBox)
class CheckBoxAdmin(admin.ModelAdmin):
    list_display = ('id', 'boxTime', 'boxEmail', 'boxCheck', 'boxMode')

@admin.register(Control)
class ControlAdmin(admin.ModelAdmin):
    list_display = ('id', 'control','device_control', 'isDo')



admin.site.site_header = '环境监测系统——上海大学毕业设计'
admin.site.site_title = '环境监测系统——上海大学 廖黄炜 李凡'

