# coding:utf-8
from django.conf.urls import patterns, include, url
from jset.views import *


urlpatterns = patterns('',
    url(r'^auth/$',                 auth_setting,           name='auth_setting'),
    url(r'^tmpl/$',                 tmpl_setting,           name='tmpl_setting'),

    url(r'^del_tmpl_name/$',        del_tmpl_name,          name='del_tmpl_name'),
    url(r'^load_tmpl_var/$',        load_tmpl_var,          name='load_tmpl_var'),
    url(r'^add_new_tmpl_name/$',    add_new_tmpl_name,      name='add_new_tmpl_name'),
    url(r'^update_tmpl_var_value/$',update_tmpl_var_value,  name='update_tmpl_var_value'),
)