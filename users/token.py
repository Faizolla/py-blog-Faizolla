from django.contrib.auth.base_user import AbstractBaseUser
from .models import User
from django.utils import six, timezone
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestamp):
        login_timestamp = timezone.datetime.timestamp(user.date_joined)
        return six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_active)+six.text_type(login_timestamp)