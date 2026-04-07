from django.core.mail import send_mail
from django.conf import settings

def send_verify_link(email, link):
    send_mail(
        subject='Email Verification',
        message=f'Please click on the link to verify your email: {link}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )