from calendar import c
from django.core.mail import send_mail
from threading import Thread
from django.conf import settings
from django.template.loader import render_to_string

from beercity.utils import email_connection

ADMIN_EMAIL = settings.SECOND_EMAIL

class SendMailThread(Thread):

    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self) -> None:
        data = self.data
        if self.data['action'] == 'contact':
            message = render_to_string('flatpages/contact_request.html', data, data['request'])
            connection = email_connection(settings)
                
            send_mail(
                "Հետադարձ կապի պատվեր", 
                message=message,
                from_email=ADMIN_EMAIL,
                recipient_list=[ADMIN_EMAIL], 
                html_message=message,
                fail_silently=True,
                connection=connection
            )
