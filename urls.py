from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'svn_admin.views.home', name='home'),
    # url(r'^svn_admin/', include('svn_admin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^$',include('login.urls')),
     url(r'^login/',include('login.urls')),
     url(r'^svn_manage/',include('svn_manage.urls')),
)
