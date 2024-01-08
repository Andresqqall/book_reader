from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from apps.auth.models import SetEmailOTC, RegisterOTC
from apps.auth.tasks import send_email_message
from apps_generic.whodidit.middleware import current_request


@receiver(post_save, sender=RegisterOTC)
@receiver(post_save, sender=SetEmailOTC)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        base_context = {
            'code': instance.code,
            'request': current_request
        }

        if isinstance(instance, SetEmailOTC):
            base_context.update(user_email=instance.email)

        elif isinstance(instance, RegisterOTC):
            base_context.update(user_email=instance.registration_try.email)

        html_message = render_to_string(
            'auth/registration/register-confirm-email.html',
            context=base_context

        )
        plain_message = strip_tags(html_message)
        send_email_message.delay(
            recipient=base_context.get('user_email', None), message=plain_message,
            html_message=html_message, subject='Confirm email'
        )
