from django.conf.urls import url
from .views import PlayListCreate


urlpatterns = [
    url(r'^playlist/create/$', PlayListCreate.as_view(), name='playlist_create'),

]