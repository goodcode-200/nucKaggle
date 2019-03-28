from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^identify',views.identify,name='identify'),
    url(r'^reset/(.*)/(.*)$',views.reset_password),
    url(r'^modify/',views.modify,name="modify"),
]