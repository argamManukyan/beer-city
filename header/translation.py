from modeltranslation.translator import TranslationOptions, register
from .models import *


@register(TopHeader)
class TopHeaderTranslationOptions(TranslationOptions):
    fields = ['title', 'url']


@register(BottomHeader)
class BottomHeaderTranslationOptions(TranslationOptions):
    fields = ['title', 'url']
