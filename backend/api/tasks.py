from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_otp(email, otp):
    send_mail(
        subject='One time password for API registration user',
        message=f'Your OTP code is: {otp}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
