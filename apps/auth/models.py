import string
import uuid

from django.contrib.auth import get_user_model
from django.core.signing import Signer
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

from apps.auth.managers import OTCManager
from apps_generic.whodidit.models import WhoDidIt

User = get_user_model()

signer = Signer(sep='.')


class RegistrationTry(models.Model):
    date = models.DateField(default=timezone.now)
    email = models.EmailField(null=True, blank=True)


class OTC(WhoDidIt):
    code = models.CharField(max_length=6, unique=True)
    applied_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(length=6, allowed_chars=string.digits)
            while self.__class__.objects.filter(code=self.code).exists():
                self.code = get_random_string(length=6, allowed_chars=string.digits)
        return super().save(*args, **kwargs)

    def apply(self, password):
        self.applied_date = timezone.now()
        self.save()


class RegisterOTC(OTC):
    objects = OTCManager()
    registration_try = models.ForeignKey(to=RegistrationTry, on_delete=models.CASCADE)

    def apply(self, password):
        if self.registration_try.email:
            user = User(email=self.registration_try.email, username=str(uuid.uuid4()))
        else:
            user = User(username=str(uuid.uuid4()))
        user.set_password(password)
        user.save()
        super().apply(password=None)
        return user


class SetEmailOTC(OTC):
    objects = OTCManager()

    email = models.EmailField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def apply(self, password):
        self.user.email = self.email
        self.user.save()
        self.user.change_password_at = timezone.now()
        super().apply(password=None)
        return self.user
