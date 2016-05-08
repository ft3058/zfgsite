# coding:utf-8
from django.conf.urls import patterns, include, url
from jset.views import *


urlpatterns = patterns('',
    url(r'^auth/$',                 auth_setting,           name='auth_setting'),
    url(r'^tmpl/$',                 tmpl_setting,           name='tmpl_setting'),

    url(r'^del_var_name/$',         del_var_name,          name='del_var_name'),
    url(r'^load_var/$',             load_var,               name='load_var'),
    url(r'^add_new_var_name/$',     add_new_var_name,      name='add_new_var_name'),
    url(r'^update_var_value/$',     update_var_value,       name='update_var_value'),
)