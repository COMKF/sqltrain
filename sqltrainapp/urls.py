from django.conf.urls import url
from django.contrib import admin
from . import views


app_name = 'sqltrainapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^questions/basic/$', views.basic, name='basic'),
    url(r'^questions/basic/selectall$', views.selectall, name='selectall')
]
