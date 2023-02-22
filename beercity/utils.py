import time
from threading import current_thread

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.deprecation import MiddlewareMixin
from django.utils.text import slugify
from unidecode import unidecode


def slug_generator(title):
    return slugify(f'{unidecode(title)}-{int(time.time())}')


class CustomModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ստեղծման օր')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ձևափոխման օր')

    class Meta:
        abstract = True


class CustomMetaModel(CustomModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)

    class Meta:
        abstract = True


class CustomLogoField(models.FileField):

    validators = [FileExtensionValidator(allowed_extensions=['svg', 'png', 'jpg'])]
    null = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'verbose_name' not in kwargs:
            self.verbose_name = 'Նկար'


def smart_strip(text):
    """ Function for strip filter fields for correct showing """
    spl_str = text.split(' ')
    new_str = ' '.join(list(filter(lambda x: len(x) > 0, spl_str)))
    return new_str


_requests = {}


def current_request():
    return _requests.get(current_thread().ident, None)


class GlobalRequestMiddleware(MiddlewareMixin):

    def process_request(self, request):
        _requests[current_thread().ident] = request