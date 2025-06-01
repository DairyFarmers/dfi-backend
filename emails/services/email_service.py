from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from typing import List, Dict, Any

class EmailService:
    @staticmethod
    def send_notification_email(
        to_email: str,
        subject: str,
        template_name: str,
        context: Dict[str, Any]
    ) -> bool:
        try:
            html_content = render_to_string(template_name, context)
            
            send_mail(
                subject=subject,
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to_email],
                html_message=html_content
            )
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False