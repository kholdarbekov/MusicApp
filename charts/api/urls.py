from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^daily/$', views.DailyChartView.as_view(), name='daily'),
]

