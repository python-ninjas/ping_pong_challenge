from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^login$',views.login),
    url(r'^logout$',views.logout),
    url(r'^register$',views.register),
    url(r'^success$',views.success),
    url(r'^userskillchart$',views.userskillchart),
    url(r'^userexpchart$',views.userexpchart),
    url(r'^userpointschart$',views.userpointschart),
    url(r'^userwinratiochart$',views.userwinratiochart),
    url(r'^home$',views.home)
    ]
