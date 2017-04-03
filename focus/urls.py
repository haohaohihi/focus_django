from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^products/(?P<page>\d+)/$', views.get_page, {'category': 'products'}, name='products_page'),
    url('^news/(?P<page>\d+)/$', views.get_page, {'category': 'news'}, name='news_page'),
    url('^design/(?P<page>\d+)/$', views.get_page, {'category': 'design'}, name='design_page'),
    url('^marketing/(?P<page>\d+)/$', views.get_page, {'category': 'marketing'}, name='marketing_page'),
    url('^dev/(?P<page>\d+)/$', views.get_page, {'category': 'development'}, name='dev'),
    url('^dev/web/(?P<page>\d+)', views.get_page, {'category': 'development', 'sub_category': 'web'},
        name='dev_web_page'),
    url('^dev/python/(?P<page>\d+)', views.get_page, {'category': 'development', 'sub_category': 'python'},
        name='dev_python_page'),
    url('^dev/linux/(?P<page>\d+)', views.get_page, {'category': 'development', 'sub_category': 'linux'},
        name='dev_linux_page'),
    url('^dev/db/(?P<page>\d+)', views.get_page, {'category': 'development', 'sub_category': 'db'},
        name='dev_db_page'),
    url('^dev/android/(?P<page>\d+)', views.get_page, {'category': 'development', 'sub_category': 'android'},
        name='dev_android_page'),
    url('^login_page$', views.login_page, name='login_page'),
    url('^login$', views.do_login, name='login'),
    url('^register$', views.do_register, name='register'),
    url('^logout$', views.do_logout, name='logout'),
    url('^add_or_cancel_collection$', views.add_or_cancel_collection, name='add_or_cancel_collection'),
    url('^my_collections/(?P<page>\d+)', views.my_collections, name='my_collections'),
]