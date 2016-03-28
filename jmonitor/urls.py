# coding:utf-8
from django.conf.urls import patterns, include, url
from jmonitor.views import *


urlpatterns = patterns('',
    url(r'^rsync/status/$', rsync_status_list, name='rsync_status_list'),  #
    url(r'^rsync/status_check/$', rsync_status_check, name='rsync_status_check'),
    url(r"^rsync/status_detail/$", rsync_status_detail, name='rsync_status_detail'),

    url(r"^oplog/status/$", oplog_status, name='oplog_status'),
)