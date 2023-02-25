from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from adminsortable2.admin import SortableAdminMixin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin
from aboutus.models import *


@admin.register(AboutUs)
class AboutUsAdmin(SingleModelAdmin, TabbedDjangoJqueryTranslationAdmin):
    pass

admin.site.register(OurGoals, TabbedDjangoJqueryTranslationAdmin)
admin.site.register(OurAdvantages, TabbedDjangoJqueryTranslationAdmin)
admin.site.register(GoalImage)
# admin.site.register(Reviews, TabbedDjangoJqueryTranslationAdmin)



@admin.register(Partners)
class PartnersAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    def get_icon(self, obj):
        if obj.icon:
            return mark_safe(f"<img src='{obj.icon.url}' height='50px' width='50px' />")
        return ''

    get_icon.short_description = 'Լոգո'
    list_display = ['name', 'get_icon']
