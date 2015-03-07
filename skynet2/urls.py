from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from Users import views as UsersView
#if not settings.DEBUG:
 #   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'skynet2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # The following 2 changes homepage to index function in Users.views
    # r'^xxxxx/' means xxxxx is required SPECIFICALLY in UNIQUE case sensitive
    # way you wrote it for the site to redirect to the link in the 2nd param

    #url(r'^$', UsersView.index, name='index'),
    url(r'^$', UsersView.index),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^Users/', include('Users.urls')), # add this new tuple
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
