from modeltranslation.translator import TranslationOptions, register
from .models import Partners


@register(Partners)
class PartnersTranslationOptions(TranslationOptions):
    fields = ['name', 'url']
