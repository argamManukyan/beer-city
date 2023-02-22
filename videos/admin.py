from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin
from .models import Video


class VideoAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass


admin.site.register(Video, VideoAdmin)