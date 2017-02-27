from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('^products/(?P<page>\d+)/$', views.products_page, name='products_page'),
    url('^news/(?P<page>\d+)/$', views.news_page, name='news_page'),
    url('^design/(?P<page>\d+)/$', views.design_page, name='design_page'),
    url('^marketing/(?P<page>\d+)/$', views.marketing_page, name='marketing_page'),
    url('^development/web/(?P<page>\d+)', views.dev_web_page, name='dev_web_page'),
    url('^development/python/(?P<page>\d+)', views.dev_python_page, name='dev_python_page'),
    url('^development/linux/(?P<page>\d+)', views.dev_linux_page, name='dev_linux_page'),
    url('^development/db/(?P<page>\d+)', views.dev_db_page, name='dev_db_page'),
    url('^development/android/(?P<page>\d+)', views.dev_android_page, name='dev_android_page'),
]