from adminsortable2.admin import SortableAdminMixin
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin
from django.contrib import admin
from .models import *


@admin.register(TopHeader)
class TopHeaderAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(BottomHeader)
class BottomHeaderAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass
