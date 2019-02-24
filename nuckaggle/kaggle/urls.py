from django.conf.urls import url
from .views import *
from django.views.static import serve
from nuckaggle import settings

urlpatterns = [
    url(r'^home',home,name='kaggle_home'),
    url(r'^racedetail/(\d+)/$',race_detail,name='race_detail'),
    url(r'^uploadfile/(\d+)/$',upload_file,name='upload_file'),
    url(r'^downloadsourcefile/(\d+)/$', dlsf, name="dlsf"),
    #下面那一行,可以让浏览器输入source文件的服务器存储地址即可见
    url(r'^media/source/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT},name="media"), 
    url(r'^dlaction/(\d+)/$', dl_action, name='dl_action'),
]