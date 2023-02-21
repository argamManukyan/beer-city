import random

from django.db import models
from django.contrib.auth.models import AbstractUser
from auditlog.registry import auditlog
from django.utils.translation import ugettext_lazy as _
from canapea.utils import CustomLogoField

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Մարզ'
        verbose_name_plural = 'Մարզեր'


class Country(models.Model):
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Քաղաք/գյուղ'
        verbose_name_plural = 'Քաղաքներ,գյուղեր'

class User(AbstractUser):

    """ Custom user model """
    ACCOUNT_TYPES = [
        ('personal', _('Ֆիզիկական')),
        ('company', _('Իրավաբանական')),
    ]

    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)  # generic field
    blocked_time = models.DateTimeField(auto_now=True)
    account_type = models.CharField(choices=ACCOUNT_TYPES, max_length=80)
    verification_code = models.CharField(max_length=10, blank=True, null=True)
    sent_verification_code = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)
    avatar = CustomLogoField(blank=True, null=True)
    attempts_count = models.PositiveSmallIntegerField(default=4)
    city = models.ForeignKey(Country,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             related_name='usercity'
                             )
    state = models.ForeignKey(State,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True,
                              related_name='userstate'
                              )
    # company data
    company_name = models.CharField(max_length=255,
                                    blank=True,
                                    null=True,
                                    verbose_name='Ընկերության անուն')
    register_city = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True,
                                      null=True, related_name='regcity',
                                      verbose_name='Ընկերության գրանցման հասցե(քաղաք)')
    register_state = models.ForeignKey(State, on_delete=models.SET_NULL,
                                       blank=True,
                                       null=True,
                                       related_name='regstate',
                                       verbose_name='Ընկերության գրանցման հասցե(մարզ)')
    register_address = models.TextField(max_length=255,
                                        blank=True,
                                        null=True,
                                        verbose_name='Ընկերության գրանցման հասցե')
    fact_city = models.ForeignKey(Country, on_delete=models.SET_NULL,
                                  blank=True,
                                  null=True,
                                  related_name='factcity',
                                  verbose_name='Ընկերության փաստացի հասցե(քաղաք)')
    fact_state = models.ForeignKey(State, on_delete=models.SET_NULL,
                                   blank=True,
                                   null=True,
                                   related_name='factstate',
                                   verbose_name='Ընկերության փաստացի հասցե(մարզ)')
    fact_address = models.CharField(max_length=255,
                                    blank=True,
                                    null=True,
                                    verbose_name='Ընկերության փաստացի հացե')
    resfirst_name = models.CharField(max_length=255,
                                     blank=True,
                                     null=True,
                                     verbose_name='Պատասխանատու անձի անուն')
    reslast_name = models.CharField(max_length=255,
                                    blank=True,
                                    null=True,
                                    verbose_name='Պատասխանատու անձի ազգանուն')
    res_position = models.CharField(max_length=255,
                                    blank=True,
                                    null=True,
                                    verbose_name='Պատասխանատու անձի պաշտոն')
    tin = models.CharField(max_length=255,
                           blank=True,
                           null=True,
                           verbose_name='ՀՎՀՀ')
    company_website = models.URLField(blank=True,
                                      null=True,
                                      verbose_name='Ընկերության ՎԵԲ կայք')
    company_spher = models.CharField(max_length=255,
                                     blank=True,
                                     null=True,
                                     verbose_name='Ընկերության ոլորտ')
    birthday = models.DateTimeField(blank=True, null=True, verbose_name='Ստեղծման/Ծննդյան օր')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.first_name

    @property
    def full_name(self):
        if self.account_type == 'personal':
            return f'{self.first_name} {self.last_name}'
        return self.company_name

    def send_otp_code(self, message_text):
        from users.services import send_otp_code
        self.verification_code = random.randrange(10000, 99999)
        self.email_verified = True
        # self.attempts_count -= 1
        print(self.verification_code)
        self.save()
        sent_code = send_otp_code(message_text, self.verification_code, self.phone_number)
        if sent_code:
            self.sent_verification_code = True
            self.save()


auditlog.register(User, exclude_fields=['password'])