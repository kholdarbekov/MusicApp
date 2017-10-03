from django.contrib.auth import views
from django.conf.urls import url
from .views import ProfileRegisterView

urlpatterns = [
    url(r'^register/$', ProfileRegisterView.as_view(), name='register'),

    url(r'^login/$', views.login, {'template_name': 'signin.html'}, name='login'),

    url(r'^logout/$', views.logout, {'next_page': 'index'}, name='logout'),

    url(r'^password/change/$', views.password_change,
        {'template_name': 'change_password.html', 'post_change_redirect': 'index'}, name='password_change'),

    url(r'^password/reset/$', views.password_reset, {'template_name': 'forgot_password.html',
                                                     'post_reset_redirect': 'index'}, name='password_reset'),

    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', views.password_reset_confirm,
        {'template_name': 'reset_password.html', 'post_reset_redirect': 'index'}, name='password_reset_confirm'),

]
