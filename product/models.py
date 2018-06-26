from django.db import models

# Create your models here.
class ProductUser(models.Model):
    userName = models.CharField(max_length=100, default='root')
    # userAge = models.