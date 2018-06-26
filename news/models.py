# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
#from django.utils.encoding import python_2_unicode_compatible
# Create your models here.


class BlogType(models.Model):  # 博客分类
    type_name = models.CharField(max_length=15)

    def __str__(self):  # 返回类型
        return self.type_name
 

class Blog(models.Model):  # 博客
    title = models.CharField(max_length=50)
    blog_types = models.ForeignKey(BlogType, on_delete=models.CASCADE)  # 外联到 博客分类
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # 外联到 User用户
    #slug = models.CharField(max_length=256, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateField(auto_now=True)

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ('-created_time',)