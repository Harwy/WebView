"""WebView URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from news.views import index,index2,echo,echo_once

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.conf.urls import url
#from . import view,testdb,search,search2
from . import view as view_home
from api import views

urlpatterns = [
    path('', view_home.home, name='home'),
    url(r'^mail/', include('mail.urls')),
    url(r'^api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('blog/', include('news.urls')),
    url(r'^index/', index),
    url(r'^index2/', index2),
    url(r'^echo$', echo),
    url(r'^echo_once', echo_once),

    #url(r'^hello$', view.hello),
    #url(r'^testdb$', testdb.testdb),
    #url(r'^search-form$', search.search_form),
    #url(r'^search$', search.search),
    #url(r'^search-post$',search2.search_post),
    # url(r'^blog/', include('blog.urls',
    #     namespace='blogs',)),
    
]

