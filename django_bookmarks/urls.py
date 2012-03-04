from django.conf.urls.defaults import *
from bookmarks.views import *

urlpatterns = patterns('',
 (r'^$', main_page),
 (r'^user/(\w+)/$', user_page),
 (r'^login/$','django.contrib.auth.views.login'),
 (r'^logout/$', logout_page),
)
