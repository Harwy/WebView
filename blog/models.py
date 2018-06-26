# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse  # django2.x把原来的 django.core.urlresolvers 包 更改为了 django.urls包
from datetime import datetime
# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                    self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', u'草稿'),
        ('published', u'已发表'),
    )
    title = models.CharField(u'标题',max_length=256)
    slug = models.SlugField(u'标签',max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                                related_name='blog_posts', on_delete=models.CASCADE,)
    body = models.TextField(u'内容')
    publish = models.DateTimeField(u'发表时间',default=timezone.now)
    created = models.DateTimeField(u'创建时间',auto_now_add=True)
    updated = models.DateTimeField(u'更新时间',auto_now=True)
    status = models.CharField(u'当前状态',max_length=10,
                                choices=STATUS_CHOICES,
                                default='draft')
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', 
            args=[self.publish.year, self.publish.strftime('%m'), self.publish.strftime('%d'), self.slug])


    class Meta:
        ordering = ('-publish',)
            
    def __str__(self):
        return self.title
