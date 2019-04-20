from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^scorelist/(.*)$',score_list,name = "score_list"),
]

