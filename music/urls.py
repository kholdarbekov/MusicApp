from django.conf.urls import url
from .views import autocomplete_view

urlpatterns = [
    url(r'^autocomplete/', autocomplete_view, name='autocomplete-view'),
]
