import json

from django.shortcuts import render, redirect
from django.contrib.gis.geoip2 import GeoIP2
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .forms import UserCreationForm
from .models import Profile
from .serializers import UserSerializer


class UserCreate(APIView):
    disallowed_countries = 'disallowed_country'
    '''
    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        """
        Check that user is from allowed regions before even bothering to
        dispatch or do other processing.
        """
        allowed_countries_codes = ['UZ', 'US', 'KR']
        g = GeoIP2()

        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR'].split(",", 1)[0].strip()
        elif 'REMOTE_ADDR' in request.META:
            ip = request.META['REMOTE_ADDR']
        else:
            ip = None
        if ip:
            country = g.country(ip)['country_code']
        else:
            country = None

        if country in allowed_countries_codes:
            return super(UserCreate, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(self.disallowed_countries)
    '''

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.get(user=user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileRegisterView(FormView):
    form_class = UserCreationForm
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
        allowed_countries_codes = ['UZ', 'US', 'KR']
        g = GeoIP2()

        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR'].split(",", 1)[0].strip()
        elif 'REMOTE_ADDR' in request.META:
            ip = request.META['REMOTE_ADDR']
        else:
            ip = None
        if ip:
            country = g.country(ip)['country_code']
        else:
            country = None

        if country in allowed_countries_codes:
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