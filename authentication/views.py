from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import TemplateView, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorator import ajax_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from .forms import UserCreationForm, UserEditForm
from .models import Profile, Follower
from .serializers import UserSerializer
from .signals import user_created


class APIUserCreate(APIView):
    http_method_names = ['post', ]
    permission_classes = [permissions.AllowAny, ]
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
            return super(APIUserCreate, self).dispatch(request, *args, **kwargs)
        else:
            return Response({'error': 'this application is not available in your country yet!'},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
    '''
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.get(user=user)
                authenticate(username=user.username, password=serializer._kwargs['data']['password1'])
                user_created.send(sender=Profile, user=user, request=request)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIUserLogin(APIView):
    http_method_names = ['post', ]
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)
        login(request=request, user=user)
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=status.HTTP_200_OK)


class ProfileRegisterView(FormView):
    form_class = UserCreationForm
    success_url = 'index'
    http_method_names = ['post', 'get']
    template_name = 'signup.html'
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
            return super(ProfileRegisterView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(self.disallowed_countries)
    '''

    def form_valid(self, form):
        if hasattr(form, 'save'):
            user = form.save()
        else:
            user = Profile.objects.create_user(**form.cleaned_data)

        user_created.send(sender=Profile, user=user, request=self.request)

        try:
            to, args, kwargs = self.get_success_url()
        except ValueError:
            return redirect(self.get_success_url())
        else:
            return redirect(to, *args, **kwargs)


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'profile.html'
    context_object_name = 'profile'
    model = Profile
    slug_field = 'username'

    def get_object(self, queryset=None):
        return Profile.objects.get(username=self.kwargs[self.slug_field])

    # def get_context_data(self, **kwargs):
    #     context = super(ProfileView, self).get_context_data(**kwargs)
    #     # context['profile'] = Profile.objects.get(pk=self.request.user.pk)
    #     return context


class UserUpdateView(UpdateView):
    form_class = UserEditForm
    model = Profile
    success_url = '/'
    template_name = 'edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@ajax_required
@require_POST
@login_required
def user_follow(request):
    usrname = request.POST.get('username')
    action = request.POST.get('action')
    if usrname and action:
        try:
            user = Profile.objects.get(username=usrname)
            if user.username != request.user.username:
                if action == 'follow':
                    Follower.objects.get_or_create(user_from=request.user, user_to=user)
                else:
                    Follower.objects.filter(user_from=request.user, user_to=user).delete()

                return JsonResponse({'status': 'ok'})
            return JsonResponse({'status': 'ko'})
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})
