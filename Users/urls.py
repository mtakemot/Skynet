__author__ = 'BCCUB002'
from django.conf.urls import patterns, url
from Users import views

urlpatterns = patterns('',
       url(r'^$', views.index, name='index'),
       url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),  # New!
       url(r'^add_category/$', views.add_category, name='add_category'), # NEW MAPPING!
       url(r'^category/(?P<category_name_url>\w+)$', views.category, name='category'),
       url(r'^register/$', views.register, name='register'), #url for register possible move to mainpage?
       url(r'^login/$', views.user_login, name='login'), #url for logging in
       url(r'^restricted/', views.restricted, name='restricted'), #url when not logged in
       url(r'^logout/$', views.user_logout, name='logout'),
       url(r'^add_package/$', views.add_package, name='add_package'),
       url(r'^display_services/$',views.display_services, name='display_services'),
       url(r'^delete_services/$',views.delete_services, name='delete_services'),
       url(r'^view_bill/$', views.view_bill, name='view_bill'),
       #url(r'market_rep/$', views.market_rep, name='market_rep'),
)
