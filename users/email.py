from django.core.mail import send_mail
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.conf import settings

admin_email = settings.EMAIL_HOST_USER


class SendMail:

    @staticmethod
    def send_activation_message(data):
        user = data.get('user')
        request = data.get('request')

        site = get_current_site(request).domain
        uid64 = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user=user)

        url = 'http://' + site + reverse('users:activate', kwargs={"uid64": uid64, 'token': token})
        recipient_list = [user.email]
        message = render_to_string('users/email/activation.html', {'user': user, 'site': site, 'link': url})

        send_mail(_('Պրոֆիլի ակտիվացում'), message, from_email=admin_email, recipient_list=recipient_list,
                  html_message=message)
        print(True)
    @staticmethod
    def send_password_reset_mail(data):
        user = data.get('user')
        request = data.get('request')

        site = get_current_site(request).domain
        uid64 = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user=user)
        request.session['password_reset_token'] = token

        url = 'http://' + site + reverse('users:password-reset-confirm', kwargs={"uid64": uid64, "token": token})
        recipient_list = [user.email]
        message = render_to_string('users/email/password-reset.html', {'user': user, 'site': site, 'link': url})

        send_mail(_('Գաղտնաբառի վերականգնում'), message, from_email=admin_email, recipient_list=recipient_list,
                  html_message=message, fail_silently=True)
