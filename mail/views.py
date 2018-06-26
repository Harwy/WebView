#coding:utf-8
"""
    邮件模块Send Email
    提供网页发送邮件功能以及发送邮件的API
"""
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template import loader
from django.conf import settings

# Create your views here.
class SendEmail():
    """send mail"""

    def ___init__(self):
        pass

    def send_html_email(self, subject, html_content, to_list):
        """发送html邮件"""
        send_from = settings.DEFAULT_FROM_EMAIL
        msg = EmailMessage(subject, html_content, send_from, to_list)
        msg.content_subtype = "html"  # 设置类型为html
        msg.send()

    def send_text_email(self, subject, body, to_list, is_fail_silently=False):
        """发送简单的文本邮件"""
        send_from = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, body, send_from, to_list, fail_silently=is_fail_silently)

    def send_email_by_template(self, subject, module, data, to_list):
        """
        使用模版发送邮件
            subject: string, 主题
            module:  string, 模版名称
            data:    dict,   数据
            to_list: list,   收件人
        """
        html_content = loader.render_to_string(module, data)
        self.send_html_email(subject, html_content, to_list)

#   邮箱警报
def setEmain(request):
    SendEmail.send_text_email('警报','警报','这是一个警报，有异常发生',['harwyliao@163.com'])
    return HttpResponse(u'发送邮件成功')

def warningHcho(request):
    SendEmail.send_text_email('警报','甲烷浓度警示','甲烷浓度超出异常',['harwyliao@163.com'])
    return HttpResponse(u'发送邮件成功')


