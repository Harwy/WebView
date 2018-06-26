from django.urls import path
from . import views

# http://39.106.213.217:8080/blog/1
# http://39.106.213.217:8080/blog/

# start with blog
urlpatterns = [
    # http://39.106.213.217:8080/blog/1
    path('',views.blog_list, name="blog_list"),
    path('<int:blog_pk>',views.blog_detail, name="blog_detail"),
    path('type/<int:blog_type_pk>', views.blogs_with_type, name="blogs_with_type"),
]
