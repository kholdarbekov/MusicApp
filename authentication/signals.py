from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth import login, get_backends
from django.dispatch import Signal
# This code is triggered whenever a new user has been created and saved to the database


user_created = Signal(providing_args=["user", "request"])


def login_user(sender, user, request, **kwargs):
    """ Automatically authenticate the user when activated  """
    backend = get_backends()[0]  # Hack to bypass `authenticate()`.
    user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    login(request, user)

user_created.connect(login_user)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        user_created.send(sender=sender, user=instance, request=kwargs['request'])
