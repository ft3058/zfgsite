# coding: utf-8

import datetime
from django.db import models
from juser.models import User, UserGroup

ASSET_ENV = (
    (1, U'生产环境'),
    (2, U'测试环境')
    )

ASSET_STATUS = (
    (1, u"已使用"),
    (2, u"未使用"),
    (3, u"报废")
    )

ASSET_TYPE = (
    (1, u"物理机"),
    (2, u"虚拟机"),
    (3, u"交换机"),
    (4, u"路由器"),
    (5, u"防火墙"),
    (6, u"Docker"),
    (7, u"其他")
    )


class AssetGroup(models.Model):
    GROUP_TYPE = (
        ('P', 'PRIVATE'),
        ('A', 'ASSET'),
    )
    name = models.CharField(max_length=80, unique=True)
    comment = models.CharField(max_length=160, blank=True, null=True)

    def __unicode__(self):
        return self.name


class AssetGroup1(models.Model):
    GROUP_TYPE = (
        ('P', 'PRIVATE'),
        ('A', 'ASSET'),
    )
    name = models.CharField(max_length=80, unique=True)
    module_path = models.CharField(max_length=6000, blank=True, null=True, verbose_name=u"分组下面的模块与路径对")
    script_path = models.CharField(max_length=500, blank=True, null=True, verbose_name=u"初始化脚本路径")
    comment = models.CharField(max_length=160, blank=True, null=True)
    group = models.ForeignKey(AssetGroup, blank=True, null=True,  on_delete=models.SET_NULL, verbose_name=u'MainGroup')

    def __unicode__(self):
        return self.name


class Domains(models.Model):
    module_name = models.CharField(max_length=30, blank=True, null=True)
    full_path = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"全路径")
    domain_host = models.CharField(max_length=30, blank=True, null=True, verbose_name=u"主服务器的ip或域名")
    port = models.IntegerField(blank=True, null=True, verbose_name=u"端口号")

    path1 = models.CharField(max_length=30, blank=True, null=True)
    path2 = models.CharField(max_length=30, blank=True, null=True)
    path3 = models.CharField(max_length=30, blank=True, null=True)
    path4 = models.CharField(max_length=30, blank=True, null=True)
    path5 = models.CharField(max_length=30, blank=True, null=True)
    path6 = models.CharField(max_length=30, blank=True, null=True)
    path7 = models.CharField(max_length=30, blank=True, null=True)
    path8 = models.CharField(max_length=30, blank=True, null=True)
    comment = models.CharField(max_length=160, blank=True, null=True)
    # asset = models.ManyToManyField(Asset, related_names="", blank=True, verbose_name=u"Asset")

    def __unicode__(self):
        s = ''  # /home
        for i in range(1, 9):
            p = ''
            exec "p = self.path%d" % i
            if p:
                s += '/' + p
        return s


class IDCParent(models.Model):
    name = models.CharField(max_length=32, verbose_name=u'机房名称')
    bandwidth = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name=u'机房带宽')
    linkman = models.CharField(max_length=16, blank=True, null=True, default='', verbose_name=u'联系人')
    phone = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name=u'联系电话')
    address = models.CharField(max_length=128, blank=True, null=True, default='', verbose_name=u"机房地址")
    network = models.TextField(blank=True, null=True, default='', verbose_name=u"IP地址段")
    date_added = models.DateField(auto_now=True, null=True)
    operator = models.CharField(max_length=32, blank=True, default='', null=True, verbose_name=u"运营商")
    comment = models.CharField(max_length=128, blank=True, default='', null=True, verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = u"IDC机房"
        verbose_name_plural = verbose_name


class IDC(IDCParent):
    pass

# class Asset(models.Model):
class AssetParent(models.Model):
    """ original asset model"""
    ip = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"主机IP")
    other_ip = models.CharField(max_length=255, blank=True, null=True, verbose_name=u"其他IP")
    hostname = models.CharField(unique=True, max_length=128, verbose_name=u"主机名")
    port = models.IntegerField(blank=True, null=True, verbose_name=u"端口号")
    group = models.ManyToManyField(AssetGroup, blank=True, verbose_name=u"所属主机组")
    username = models.CharField(max_length=16, blank=True, null=True, verbose_name=u"管理用户名")
    password = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"密码")
    use_default_auth = models.BooleanField(default=True, verbose_name=u"使用默认管理账号")
    idc = models.ForeignKey(IDC, blank=True, null=True,  on_delete=models.SET_NULL, verbose_name=u'机房')
    mac = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"MAC地址")
    remote_ip = models.CharField(max_length=16, blank=True, null=True, verbose_name=u'远控卡IP')
    brand = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'硬件厂商型号')
    cpu = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'CPU')
    memory = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'内存')
    disk = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'硬盘')
    system_type = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"系统类型")
    system_version = models.CharField(max_length=8, blank=True, null=True, verbose_name=u"系统版本号")
    system_arch = models.CharField(max_length=16, blank=True, null=True, verbose_name=u"系统平台")
    cabinet = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'机柜号')
    position = models.IntegerField(blank=True, null=True, verbose_name=u'机器位置')
    number = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'资产编号')
    status = models.IntegerField(choices=ASSET_STATUS, blank=True, null=True, default=1, verbose_name=u"机器状态")
    asset_type = models.IntegerField(choices=ASSET_TYPE, blank=True, null=True, verbose_name=u"主机类型")
    env = models.IntegerField(choices=ASSET_ENV, blank=True, null=True, verbose_name=u"运行环境")
    sn = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"SN编号")
    date_added = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name=u"是否激活")
    comment = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"备注")

    def __unicode__(self):
        return self.ip

    class Meta:
        abstract = True
        ordering = ['-date_added']


class Asset(AssetParent):
    # add new fields
    check_code = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'CheckCode')
    passwd = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'Passwordforview')
    udate = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name=u'UpdateDate')
    project = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'Project')
    type1 = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'Type1')
    type2 = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'Type2')
    group1 = models.ManyToManyField(AssetGroup1, blank=True, verbose_name=u"所属分组")
    domains = models.ManyToManyField(Domains, blank=True, verbose_name=u"Domain")
    area = models.CharField(max_length=1, blank=True, null=True, verbose_name=u'国内:c, 国外:f')
    comm_name = models.CharField(max_length=10, blank=True, null=True, verbose_name=u'snmp community name,yxdown,youxun,unknown')

    def get_username(self):
        """restore password by passwd"""
        from jumpserver.api import CRYPTOR
        if self.username:
            return self.username
        else:
            self.username = 'root'
            if not self.password and self.passwd:
                self.password = CRYPTOR.encrypt(self.passwd)
            self.save()
            return 'root'


class AssetRecord(models.Model):
    asset = models.ForeignKey(Asset)
    username = models.CharField(max_length=30, null=True)
    alert_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)


class AssetAlias(models.Model):
    user = models.ForeignKey(User)
    asset = models.ForeignKey(Asset)
    alias = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.alias

class IpInfo(models.Model):
    """
    {
      "ip": "218.75.155.46",
      "hostname": "No Hostname",
      "city": "Changsha",
      "region": "Hunan",
      "country": "CN",
      "loc": "28.1792,113.1136",
      "org": "AS4134 No.31,Jin-rong Street"
    }
    """
    ip = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'ip')
    hostname = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'hostname')
    city = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'city')
    region = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'region')
    country = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'country')
    loc = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'loc')
    org = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'org')
    comment = models.TextField(null=True, blank=True)
    cdt = models.DateTimeField(auto_now=True, null=True)
    asset = models.ForeignKey(Asset)