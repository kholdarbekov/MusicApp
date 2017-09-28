from .models import Profile


class EmailAuthBackend(object):
    """
    Authenticate using e-mail account.
    """
    def authenticate(self, username=None, password=None):
        try:
            user = Profile.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except Profile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Profile.objects.get(pk=user_id)
        except Profile.DoesNotExist:
            return None