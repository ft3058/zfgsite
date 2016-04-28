# coding:utf8
from django.db import models

# Create your models here.

class TcpConnCount(models.Model):
    ip = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"主机IP")
    cnt = models.IntegerField(blank=True, null=True)
    cdt = models.DateTimeField(auto_now=True, null=True)



