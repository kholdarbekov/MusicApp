from django.conf.urls import url
from charts import views

urlpatterns = [
    url(r'^update-charts/$', views.update_charts, name='update_charts'),
]
