from django.db import models


class Log(models.Model):
    user = models.CharField(max_length=20, null=True)
    host = models.CharField(max_length=200, null=True)
    remote_ip = models.CharField(max_length=100)
    login_type = models.CharField(max_length=100)
    log_path = models.CharField(max_length=100)
    start_time = models.DateTimeField(null=True)
    pid = models.IntegerField()
    is_finished = models.BooleanField(default=False)
    end_time = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.log_path


class Alert(models.Model):
    msg = models.CharField(max_length=20)
    time = models.DateTimeField(null=True)
    is_finished = models.BigIntegerField(default=False)


class TtyLog(models.Model):
    log = models.ForeignKey(Log)
    datetime = models.DateTimeField(auto_now=True)
    cmd = models.CharField(max_length=200)


class ExecLog(models.Model):
    user = models.CharField(max_length=100)
    host = models.TextField()
    cmd = models.TextField()
    remote_ip = models.CharField(max_length=100)
    result = models.TextField(default='')
    datetime = models.DateTimeField(auto_now=True)


class FileLog(models.Model):
    user = models.CharField(max_length=100)
    host = models.TextField()
    filename = models.TextField()
    type = models.CharField(max_length=20)
    remote_ip = models.CharField(max_length=100)
    result = models.TextField(default='')
    datetime = models.DateTimeField(auto_now=True)


class RsyncCheckLog(models.Model):
    user = models.CharField(max_length=100)
    host = models.TextField(max_length=50, null=True)
    cmd = models.TextField(null=True)
    remote_ip = models.CharField(max_length=100, null=True)
    result = models.TextField(default='', null=True)
    datetime = models.DateTimeField(auto_now=True, null=True)

    check_status = models.CharField(max_length=10, null=True)
    file_num = models.TextField(default='', null=True)
    file_not_exists = models.TextField(default='', null=True)
    file_err_time = models.TextField(default='', null=True)
    file_err_size = models.TextField(default='', null=True)
    exec_seconds = models.CharField(max_length=10, null=True)
    result_tag = models.CharField(max_length=10, null=True)


class CustomLog(models.Model):
    user = models.CharField(max_length=100, default='', null=True)
    host = models.TextField(default='', null=True)
    ip = models.CharField(max_length=100, default='', null=True)
    cmd = models.TextField(default='', null=True)
    title = models.CharField(max_length=50, default='', null=True)
    result = models.TextField(default='', null=True)
    datetime = models.DateTimeField(auto_now=True)



