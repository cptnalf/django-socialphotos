from django.conf.urls import patterns, url

urlpatterns = patterns('spt.views',
                       url(r'^$', 'index'),
                       url(r'^photos/(?P<photo_slug>[a-zA-Z0-9._-]+)/$', 'photo_detail'),
                       url(r'^tags/$', 'tags_list'),
                       url(r'^tags/(?P<tag_slug>[a-zA-Z0-9._-]+)/$', 'tag_detail'),
                       )
