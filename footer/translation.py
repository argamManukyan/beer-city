from modeltranslation.translator import TranslationOptions, register


from .models import *


@register(FooterCategory)
class FooterCategoryTranslationOptions(TranslationOptions):
    fields = ['title']


@register(Footer)
class FooterTranslationOptions(TranslationOptions):
    fields = ['title', 'url']


@register(SocialIcons)
class SocialIconsTranslationOptions(TranslationOptions):
    fields = ['title', 'url']


@register(BankIcons)
class BankIconsTranslationOptions(TranslationOptions):
    fields = ['title', 'url']


@register(PersonalData)
class PersonalDataTranslationOptions(TranslationOptions):
    fields = ['text', 'url']
