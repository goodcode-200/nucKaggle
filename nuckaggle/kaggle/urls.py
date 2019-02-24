from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^home',home,name='kaggle_home'),
    url(r'^racedetail/(\d+)/$',race_detail,name='race_detail'),
    url(r'^uploadfile/(\d+)/$',upload_file,name='upload_file'),
]