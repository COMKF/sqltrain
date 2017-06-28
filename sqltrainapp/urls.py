from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'sqltrainapp'
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login_detail/$', views.login_detail, name='login_detail'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register_detail/$', views.register_detail, name='register_detail'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^index/$', views.index, name='index'),
    url(r'^Getting_Started/$', views.Getting_Started, name='Getting_Started'),
    url(r'^basic/$', views.basic, name='basic'),
    url(r'^joins/$', views.joins, name='joins'),
    url(r'^aggregates/$', views.aggregates, name='aggregates'),
    url(r'^date/$', views.date, name='date'),
    url(r'^string/$', views.string, name='string'),
    url(r'^recursive/$', views.recursive, name='recursive'),

    url(r'^moban/$', views.moban, name='moban'),

    url(r'^about/$', views.about, name='about'),
    url(r'^options/$', views.options, name='options'),
    # url(r'^Getting_Started/$', views.Getting_Started, name='Getting_Started'),
    # url(r'^Getting_Started/$', views.Getting_Started, name='Getting_Started'),
    # url(r'^Getting_Started/$', views.Getting_Started, name='Getting_Started'),
    # url(r'^$', admin.site.urls),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    # url(r'templates/polls/add/$', views.addView.as_view(), name='add'),
    # url(r'templates/polls/question/$', views.questionView.as_view(), name='question'),
]

