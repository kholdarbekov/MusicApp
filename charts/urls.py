from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from charts import views

urlpatterns = [
    url(r'^daily/$', views.DailyChartView.as_view(), name='daily'),
    url(r'^update-charts/$', views.update_charts, name='update_charts'),
    # url(r'^musics/(?P<pk>[0-9]+)/$', views.MusicPlay.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
