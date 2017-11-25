from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^daily/$', views.ChartView.as_view(), name='daily'),
]
