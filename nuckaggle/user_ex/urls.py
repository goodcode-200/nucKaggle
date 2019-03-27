from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^identify',views.identify,name='identify'),
]