from django.conf.urls import patterns, include, url
from FindMyProfessor.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^data/(.*)$', displaydatadb),
    url(r'^database$', printDatabase),
    url(r'^insertdata$', insertData),
    url(r'^search/$', search),
    url(r'^addofficehourssubmit/(.*)$', addofficehourssubmit),
    url(r'^officehours/(.*)$', addofficehours),

)
