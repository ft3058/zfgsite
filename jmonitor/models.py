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


class AssetBiz(models.Model):
    ip = models.CharField(max_length=32, blank=True, null=True)
    group1_name = models.CharField(max_length=64, blank=True, null=True)
    origin_biz = models.CharField(max_length=500, blank=True, null=True)
    current_biz = models.CharField(max_length=500, blank=True, null=True)
    ifmatch = models.CharField(max_length=1, blank=True, null=True)
    status = models.TextField(null=True, blank=True)
    cdt = models.DateTimeField(auto_now=True, null=True)