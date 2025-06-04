from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from users.models import User, Passcode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.encoding import smart_bytes
from django.conf import settings
from utils import setup_logger

logger = setup_logger(__name__)

class EmailSender:      
    def send_email(self, email, subject, plain_message, html_message):
        try:
            email = EmailMultiAlternatives(
                subject,
                plain_message, 
                settings.EMAIL_HOST_USER,
                [email],            )
            email.attach_alternative(html_message, "text/html")
            email.send()
        except Exception as e:
            logger.error(f"Error sending an email: {e}")