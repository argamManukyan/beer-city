from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from beercity.utils import CustomLogoField


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Մարզ'
        verbose_name_plural = 'Մարզեր'


class Region(models.Model):
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Քաղաք/գյուղ'
        verbose_name_plural = 'Քաղաքներ,գյուղեր'


class User(AbstractUser):

    email = models.EmailField(unique=True)
    blocked_time = models.DateTimeField(auto_now=True)
    verification_code = models.CharField(max_length=10, blank=True, null=True)
    sent_verification_code = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)
    avatar = CustomLogoField(blank=True, null=True)
    city = models.ForeignKey(Region,
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
    
    birthday = models.DateTimeField(blank=True, null=True, verbose_name='Ստեղծման/Ծննդյան օր')
    bonuses_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.full_name or self.email

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'