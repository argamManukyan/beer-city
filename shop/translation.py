from modeltranslation.translator import TranslationOptions, register

from aboutus.models import OurGoals, AboutUs, Reviews, OurAdvantages
from flatpages.models import FlatPages, Blog, BlogCategory, GalleryCategory, FAQModel
from .models import *
from users.models import State, Country
from breadcrumbs.models import BreadcrumbTexts


@register(AboutUs)
class AboutsTrans(TranslationOptions):
    fields = ['text']
    
    
@register([OurGoals, Reviews, OurAdvantages])
class OurGoalsTrans(TranslationOptions):
    fields = ['name', 'text']


@register(FAQModel)
class FAQTranslate(TranslationOptions):
    fields = ['question', 'answer']

@register([BlogCategory, GalleryCategory])
class StateTranslation(TranslationOptions):
    fields = ['name', 'breadcrumb_text', 'meta_title', 'meta_description']


@register(Blog)
class StateTranslation(TranslationOptions):
    fields = ['name', 'large_text', 'short_text', 'meta_title', 'meta_description']


@register([Country, Brand])
class CountryTranslation(TranslationOptions):
    fields = ['name',]


@register(UnitMeasurement)
class UnitMeasurementTranslation(TranslationOptions):
    fields = ['title',]


@register(BreadcrumbTexts)
class BreadcrumbTextsTranslation(TranslationOptions):
    fields = ['breadcrumbs_text', 'page_title']


@register(FlatPages)
class FlatpagesTranslation(TranslationOptions):
    fields = ['page_name', 'content', 'meta_title', 'meta_description']

@register(Slider)
class SliderTranslationOptions(TranslationOptions):
    fields = ['text', 'url']


@register(BonusDays)
class BonusDaysTranslationOptions(TranslationOptions):
    fields = ['title']


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = [
        'name',
        'short_description',
        'meta_title',
        'meta_description'
    ]


@register(FilterField)
class FilterFieldTranslationOptions(TranslationOptions):
    fields = ['title', 'help_field_title', 'help_field_content']


@register(FilterValue)
class FilterValueTranslationOptions(TranslationOptions):
    fields = ['title']


@register(Bullets)
class BulletsTranslationOptions(TranslationOptions):
    fields = ['title', 'text']


@register(HomepageBanners)
class HomepageBannersTranslationOptions(TranslationOptions):
    fields = ['name', 'url', 'description']


@register(Color)
class ColorTranslationOptions(TranslationOptions):
    fields = ['title']


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ['name', 'large_description', 'meta_title', 'meta_description']