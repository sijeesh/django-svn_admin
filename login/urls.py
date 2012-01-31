from django.conf.urls.defaults import patterns, include, url
from login.views import *

urlpatterns=patterns('',

 url(r'^$',login_page),
 url(r'^login_to$',login_to),
 url(r'^logout$',logout),
 url(r'^home$',home),

)
