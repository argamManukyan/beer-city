from adminsortable2.admin import SortableAdminMixin
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin
from django.contrib import admin
from .models import *


@admin.register(TopHeader)
class TopHeaderAdmin(TabbedDjangoJqueryTranslationAdmin, SortableAdminMixin, admin.ModelAdmin):
    pass


@admin.register(BottomHeader)
class BottomHeaderAdmin(TabbedDjangoJqueryTranslationAdmin, SortableAdminMixin, admin.ModelAdmin):
    pass
