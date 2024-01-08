from django.core.mail import send_mail

from book_reader.celery import app


@app.task
def send_email_message(subject, message, recipient, html_message):
    return send_mail(
        subject=subject,
        message=message,
        recipient_list=[recipient],
        fail_silently=False,
        from_email=None,
        html_message=html_message
    )
