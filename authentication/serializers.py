from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.conf import settings
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=Profile.objects.all())]
            )
    username = serializers.CharField(max_length=64,
            validators=[UniqueValidator(queryset=Profile.objects.all())]
            )
    password1 = serializers.CharField(min_length=settings.PASSWORD_MINIMUM_LENGTH, write_only=True)
    password2 = serializers.CharField(min_length=settings.PASSWORD_MINIMUM_LENGTH, write_only=True)

    def validate_password2(self, value):
        password1 = self.initial_data['password1']
        if password1 != value:
            raise serializers.ValidationError("Passwords don't match: password1: %s, password2: %s" % (password1, value))
        elif not password1 or not value:
            raise serializers.ValidationError("You should fill both password fields")
        return value

    def create(self, validated_data):
        user = Profile.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password1'])
        return user

    class Meta:
        model = Profile
        fields = ('username', 'email', 'password1', 'password2')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username', 'photo')
