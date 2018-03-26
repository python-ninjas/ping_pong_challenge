from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^game$',views.play),
    url(r'^result$',views.result)
    ]