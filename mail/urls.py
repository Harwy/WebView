from django.conf.urls import url
from . import views as views_mail

urlpatterns = [
    url(r'^mail', views_mail.setEmain),
    url(r'^hcho', views_mail.warningHcho),
]

