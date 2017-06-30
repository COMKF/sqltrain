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

    url(r'^basic/(?P<question_id>[0-9]+)/$', views.basicall, name='basicall'),
    url(r'^basic/result$', views.result, name='result'),

    url(r'^moban/$', views.moban, name='moban'),

    url(r'^about/$', views.about, name='about'),
    url(r'^options/$', views.options, name='options'),

    #个人信息，后台页面
    url(r'^personinfo/(?P<user_name>.+)/$', views.personinfo, name='personinfo'),
    url(r'^changeinfo/$', views.changeinfo, name='changeinfo'),
    url(r'^changepwd/$', views.changepwd, name='changepwd'),
    url(r'^changepwd_detail/$', views.changepwd_detail, name='changepwd_detail'),

    # 管理员视图
    url(r'^A_manage_T/$', views.A_manage_T, name='A_manage_T'),
    url(r'^revoke_T/(?P<user_id>.+)/$', views.revoke_T, name='revoke_T'),
    url(r'^A_manage_S/$', views.A_manage_S, name='A_manage_S'),
    url(r'^promote_S/(?P<user_id>.+)/$', views.promote_S, name='promote_S'),
    url(r'^delete/(?P<user_id>.+)/$', views.delete, name='delete'),
    url(r'^A_select_T/$', views.A_select_T, name='A_select_T'),
    url(r'^A_select_S/$', views.A_select_S, name='A_select_S'),

    # 教师视图
    url(r'^T_show_S/$', views.T_show_S, name='T_show_S'),
    url(r'^T_show_Q/$', views.T_show_Q, name='T_show_Q'),
    # url(r'^submitques/$', views.submitques, name='submitques'),


    # 学生视图
    url(r'^S_pass_Q/$', views.S_pass_Q, name='S_pass_Q'),
    url(r'^S_fail_Q/$', views.S_fail_Q, name='S_fail_Q'),
    url(r'^S_his/$', views.S_his, name='S_his'),

    # 查询
    # url(r'^A_select_T/$', views.A_select_T, name='A_select_T'),
    url(r'^T_select_S/$', views.T_select_S, name='T_select_S'),
    url(r'^T_select_Q/$', views.T_select_Q, name='T_select_Q'),

    # url(r'^$', admin.site.urls),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    # url(r'templates/polls/add/$', views.addView.as_view(), name='add'),
    # url(r'templates/polls/question/$', views.questionView.as_view(), name='question'),
]

