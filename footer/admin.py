from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin
from .models import *


@admin.register(Footer)
class FooterAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(SocialIcons)
class SocialIconsAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    def get_icon(self, obj):
        if obj.icon:
            return mark_safe("<img src='{}' height='50px' width='50px' />".format(obj.icon.url))
        return ''

    get_icon.short_description = 'Լոգո'
    list_display = ['title', 'get_icon']


@admin.register(BankIcons)
class BankIconsAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):

    def get_icon(self, obj):
        if obj.icon:
            return mark_safe("<img src='{}' height='50px' width='50px' />".format(obj.icon.url))
        return ''

    get_icon.short_description = 'Լոգո'
    list_display = ['title', 'get_icon']


@admin.register(FooterCategory)
class FooterCategoryAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass

@admin.register(PersonalData)
class PersonalDataAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    def get_icon(self, obj):
        if obj.icon:
            return mark_safe(f"<img src='{obj.icon.url}' height='50px' width='50px' />")
        return ''

    get_icon.short_description = 'Լոգո'
    list_display = ['text', 'get_icon']
