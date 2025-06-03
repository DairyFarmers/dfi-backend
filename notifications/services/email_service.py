from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from utils import EmailSender
from utils import setup_logger

logger = setup_logger(__name__)

class EmailService:
    def __init__(self):
        self.current_site = settings.TRUSTED_ORIGIN
        
    def send_email(
        self,
        recp_email,
        recp_name,
        subject,
        title,
        message
    ):
        try:
            html_message = render_to_string(
                'emails/notification.html', 
            {
                'current_site': self.current_site,
                'recipient_name': recp_name,
                'title': title,
                'message': message,
            })
            plain_message = strip_tags(html_message)
            EmailSender.send_email(
                recp_email,
                subject,
                plain_message,
                html_message
            )
        except Exception as e:
            logger.error(f"Failed to send notification email: {str(e)}")
            return False
        
    def send_product_expiry_email(
        self,
        recp_email,
        recp_name,
        priority,
        title,
        message
    ):
        try:
            html_message = render_to_string(
                'emails/product_expiry.html', 
            {
                'current_site': self.current_site,
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
        except Exception as e:
            logger.error(f"Failed to send product expiry email: {str(e)}")
            return False
        
    def send_welcome_email(
        self, 
        recp_email, 
        recp_name,
        title,
        message, 
        role
    ) -> bool:
        try:
            html_message = render_to_string(
                'emails/welcome_email.html', 
            {
                'current_site': self.current_site,
                'recipient_name': recp_name,
                'title': title,
                'message': message,
            })
            plain_message = strip_tags(html_message)
            EmailSender.send_email(
                recp_email,
                'Welcome to Dairy Farmers!',
                plain_message,
                html_message
            )
        except Exception as e:
            logger.error(f"Failed to send welcome email: {str(e)}")
            return False