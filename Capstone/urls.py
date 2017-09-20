"""Capstone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import TemplateView

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)


urlpatterns = [
    url(r'^', include('charts.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^genres/$', TemplateView.as_view(template_name='genres.html'), name='genres'),
    url(r'^profile/$', TemplateView.as_view(template_name='profile.html'), name='profile'),
    url(r'^change-password/$', TemplateView.as_view(template_name='change_password.html'), name='change_password'),
    url(r'^forgot-password/$', TemplateView.as_view(template_name='forgot_password.html'), name='forgot_password'),
    url(r'^listen/$', TemplateView.as_view(template_name='listen.html'), name='listen'),
    url(r'^reset-password/$', TemplateView.as_view(template_name='reset_password.html'), name='reset_password'),
    url(r'^sign-in/$', TemplateView.as_view(template_name='signin.html'), name='signin'),
    url(r'^sign-up/$', TemplateView.as_view(template_name='signup.html'), name='signup'),
    url(r'^change-password/$', TemplateView.as_view(template_name='change_password.html')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)