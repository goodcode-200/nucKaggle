from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^login/',user_login,name='login'),
    url(r'^register/',register,name='register'), 
    url(r'^logout/',user_logout,name='logout'), 
    url(r'^team/',team,name='team'),
    url(r'^createteam/',create_team,name='create_team'),
    url(r'^entercom/',enter_com,name='enter_com'),
    url(r'^jointeam/',join_team,name='join_team'),
    url(r'^joinreq/(\d+)/(\d)/$',join_req,name='join_req'),
    url(r'^invite/(\d+)/(\d)/(\d+)/$',invite,name='invite'),
    url(r'^reqdeal/',req_deal,name='req_deal'),
    url(r'^agree/(\d+)$',agree,name='agree'),
    url(r'^personcenter',person_center,name="person_center"),
    url(r'^confirm/(\d+)',confirm,name="confirm"),
    url(r'^alter1submit',alter1_submit,name="alter1_submit"),
    url(r'^alter2submit',alter2_submit,name="alter2_submit"),
    url(r'^give_up_alter',give_up_alter,name="give_up_alter"),
    url(r'^captaintrans',captain_trans,name="captain_trans"),
    url(r'^delordisteam',del_ordisteam,name="del_ordisteam"),
    url(r'^disenterteam/(\d+)/(\d+)',dis_enter_team,name="dis_enter_team"),
]
