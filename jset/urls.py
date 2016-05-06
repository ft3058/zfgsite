# coding:utf-8
from django.conf.urls import patterns, include, url
from jset.views import *


urlpatterns = patterns('',
    url(r'^auth/$', auth_setting, name='auth_setting'),  #
    url(r'^tmpl/$', tmpl_setting, name='tmpl_setting'),  #
)