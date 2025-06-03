from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from utils import EmailSender

class EmailService:    
    def send_product_expiry_email(
        self,
        recp_email,
        recp_name,
        priority,
        title,
        message
    ):
        current_site = settings.TRUSTED_ORIGIN
        html_message = render_to_string(
            'emails/product_expiry.html', 
        {
            'current_site': current_site,
            'recipient_name': recp_name,
            'priority': priority,
            'title': title,
            'message': message,
        })
        plain_message = strip_tags(html_message)
        EmailSender.send_email(
            recp_email,
            'Product Expiry Notification',
            plain_message,
            html_message
        )