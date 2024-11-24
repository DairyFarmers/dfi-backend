from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

class EmailService:
    def __init__(self, email_sender):
        self.email_sender = email_sender
        
    def send_passcode_email(self, user, passcode):
        current_site = settings.TRUSTED_ORIGIN
        html_message = render_to_string('emails/passcode_email.html', {
            'current_site': current_site,
            'recipient_name': user.first_name, 
            'otp': passcode
        })
        plain_message = strip_tags(html_message)
        self.email_sender.send_email(
            user.email,
            'SecBot Email Verification Code',
            plain_message,
            html_message
        )