from modeltranslation.translator import TranslationOptions, register

from .models import Video


@register(Video)
class VideoTranslator(TranslationOptions):
    fields = ['text']