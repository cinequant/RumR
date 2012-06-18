from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     url(r'^polls/$', 'polls.views.index'),
     url(r'^polls/(?P<poll_id>\d+)/$', 'polls.views.detail'),	
    # Examples:
     url(r'^$', 'mysite.views.home', name='home'),
     url(r'^mysite/', include('mysite.foo.urls')),
     url(r'^polls/notation', 'polls.views.notation')

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
