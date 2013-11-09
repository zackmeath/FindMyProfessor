from django.conf.urls import patterns, include, url
from FindMyProfessor.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)), 
    url(r'^$', index), #homepage
    url(r'^data/(.*)$', displaydatadb), #show data of the professor in url
    url(r'^database$', printDatabase), #show the raw database information (for debugging and testing only)
    url(r'^insertdata$', insertData), #Insert the data into the database (only for after killing the database)
    url(r'^search/$', search), #Page that loads when user searches for a professor
    url(r'^addofficehourssubmit/(.*)$', addofficehourssubmit), #when user submits the addofficehours form
    url(r'^officehours/(.*)$', addofficehours), #form to fill out for office hours
    url(r'^comment/(.*)$', comment), #form to fill out for comments
    url(r'^submitcomment/(.*)$', submitcomment), #when user submits comment form


)
