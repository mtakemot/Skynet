from django.conf.urls import patterns, include, url
#from django.conf.urls import settings
from django.contrib import admin
from django.conf.urls.static import static

#if not settings.DEBUG:
 #   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'skynet2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^Users/', include('Users.urls')), # add this new tuple
)
