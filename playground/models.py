from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class WebsiteUser(models.Model):
    first_name = models.CharField('first name', max_length=30)
    last_name = models.CharField('last name', max_length=30)
    email = models.EmailField('email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Info(models.Model):
    name = models.CharField('info name', max_length=120)
    publisher_name = models.CharField('publisher name', blank=True, null=True, max_length=60)
    publisher = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    info = models.TextField(max_length=2000)

    def __str__(self):
        return self.name
