from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Webuser(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=10, null=True, blank=True)
    hospital = models.CharField(max_length=20, null=True, blank=True)
    position = models.CharField(max_length=10, null=True, blank=True)
    department = models.CharField(max_length=10, null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    abstract = models.TextField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.user.username

class Project(models.Model):
    user = models.ForeignKey(User)
    Order_ID =  models.CharField(primary_key=True,max_length=30, null=False, blank=False)
    name = models.CharField(max_length=50, null=True, blank=True)
    classify = models.CharField(max_length=10, null=True, blank=True)
    upload_dir = models.CharField(max_length=5000, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    status =models.BooleanField(default=False)
    remark = models.TextField(max_length=100, null=True)
    def __unicode__(self):
        return self.user.username

class UploadFile(models.Model):
    user = models.ForeignKey(User)
    Order_ID =  models.ForeignKey(Project)
    directory = models.CharField(primary_key=True,max_length=100, null=False, blank=False)
    upload_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.user.username

class Pay(models.Model):
    project = models.OneToOneField(Project)
    user = models.ForeignKey(User)
    is_pay = models.BooleanField(default=False)
    price = models.CharField(max_length=10, null=True, blank=True)

    def __unicode__(self):
        return self.user.username