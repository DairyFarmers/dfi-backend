from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes

class EmailService:
    def __init__(self, email_sender):
        self.email_sender = email_sender
        
    def send_passcode_email(self, user, passcode):
        current_site = settings.TRUSTED_ORIGIN
        html_message = render_to_string('emails/passcode_email.html', {
            'current_site': current_site[0],
            'recipient_name': user.first_name, 
            'otp': passcode
        })
        plain_message = strip_tags(html_message)
        self.email_sender.send_email(
            user.email,
            'Dairy Inventory App Email Verification Code',
            plain_message,
            html_message
        )
        
    def send_password_reset_email(self, user, token):
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))        
        current_site = settings.TRUSTED_ORIGIN
        relative_link = f'/password-reset/{uidb64}/{token}'
        absolute_link=f"{current_site}{relative_link}"
        html_message = render_to_string('emails/password_reset.html', {
            'current_site': current_site,
            'recipient_name': user.first_name, 
            'link': absolute_link
        })
        plain_message = strip_tags(html_message)
        self.email_sender.send_email(
            user.email,
            'Dairy Inventory App Password Reset Link',
            plain_message,
            html_message
        )