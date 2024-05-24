from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import *
from django.core.mail import send_mail
from django.utils import timezone

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            pass
        else:
            otp.objects.create(user=instance, exp=timezone.now() + timezone.timedelta(minutes=5))
            instance.is_active=True
            instance.save()

         
            #email verification 
            otpc  = otp.objects.filter(user=instance).last()
            subject = "Email Verification"
            message = f"""

                                Hi {instance.username}, welcome to jettrade the most trusted and fastest crypto and giftcard buying and selling platform. Please use the otp code provided to verify your account thank you. {otpc.code1} this codes expires in 5 minute. http://127.0.0.1:8000/emailverification/{instance.username}

                                """
            sender = "test@kcls-swift.com"
            receiver = [instance.email, ]


            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )


def send_admin_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New User Registration'
        message = 'A new user has registered in your web app. Username: {}'.format(instance.username)
        admin_email = 'itzpromiz@gmail.com'  # Change this to your admin email
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])