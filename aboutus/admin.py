from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin
from aboutus.models import *


@admin.register(AboutUs)
class AboutUsAdmin(SingleModelAdmin, TabbedDjangoJqueryTranslationAdmin):
    pass

admin.site.register(OurGoals, TabbedDjangoJqueryTranslationAdmin)
admin.site.register(OurAdvantages, TabbedDjangoJqueryTranslationAdmin)
admin.site.register(GoalImage)
admin.site.register(Reviews, TabbedDjangoJqueryTranslationAdmin)