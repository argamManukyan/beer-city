from modeltranslation.translator import register, TranslationOptions

from .models import *


@register([EmploymentTerm, JobType, Location])
class JobDetailsTranslations(TranslationOptions):
    fields = ['title']


@register(JobCategory)
class JobCategoryTranslation(TranslationOptions):
    fields = ['name', 'breadcrumbs_text', 'meta_title', 'meta_description']


@register(JobItem)
class JobItemTranslation(TranslationOptions):
    fields = ['name', 'short_description', 'large_description', 'meta_title', 'meta_description']

