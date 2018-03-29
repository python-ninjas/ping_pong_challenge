from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^play$',views.play),
    url(r'^result$',views.result),
    url(r'^stats$',views.stats),
    url(r'^stats/load$',views.load_stats),
    url(r'^stats/find$',views.find_stats)
    ]