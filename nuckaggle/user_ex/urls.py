from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^identify',views.identify,name='identify'),
    url(r'^reset/<str:active_code>',ResetView.as_view(),name='reset'),
]