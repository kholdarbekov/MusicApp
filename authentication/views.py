from django.shortcuts import render, redirect
from django.contrib.gis.geoip2 import GeoIP2
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters

from .forms import ProfileForm
from .models import Profile
# Create your views here.


class ProfileRegisterView(FormView):
    form_class = ProfileForm
    success_url = 'index'
    http_method_names = ['post', 'get']
    template_name = 'signup.html'
    disallowed_countries = 'disallowed_country'

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        """
        Check that user is from allowed regions before even bothering to
        dispatch or do other processing.
        """
        allowed_countries = ['Uzbekistan', 'United States', 'Korea', 'Germany']
        g =GeoIP2()

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        if ip:
            country = g.country(ip)['country_name']
        else:
            country = None

        if country in allowed_countries:
            return super(ProfileRegisterView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(self.disallowed_countries)

    def form_valid(self, form):
        if hasattr(form, 'save'):
            form.save()
        else:
            Profile.objects.create_user(**form.cleaned_data)

        try:
            to, args, kwargs = self.get_success_url()
        except ValueError:
            return redirect(self.get_success_url())
        else:
            return redirect(to, *args, **kwargs)