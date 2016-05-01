# coding:utf8
from django.db import models


class TcpConnCount(models.Model):
    ip = models.CharField(max_length=32, blank=True, null=True)
    cnt = models.IntegerField(blank=True, null=True)
    cdt = models.DateTimeField(auto_now=True, null=True)


class DiskSize(models.Model):
    ip = models.CharField(max_length=32, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    used = models.IntegerField(blank=True, null=True)
    cdt = models.DateTimeField(auto_now=True, null=True)

class InterfaceIo(models.Model):
    ip = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=10, blank=True, null=True)
    insize = models.BigIntegerField(blank=True, null=True)
    outsize = models.BigIntegerField(blank=True, null=True)
    cdt = models.DateTimeField(auto_now=True, null=True)