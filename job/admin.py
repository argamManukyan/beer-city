from django.contrib import admin
from django.utils.safestring import mark_safe

from canapea.settings import STATIC_URL
from .models import *
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin

admin.site.register(JobType, TabbedDjangoJqueryTranslationAdmin)
admin.site.register(Location, TabbedDjangoJqueryTranslationAdmin)
admin.site.register(EmploymentTerm, TabbedDjangoJqueryTranslationAdmin)
admin.site.register(JobCategory, TabbedDjangoJqueryTranslationAdmin)


@admin.register(SubmittedResumes)
class SubmittedResumesAdmin(admin.ModelAdmin):
    list_display = ['id', 'job_title']

    def get_created(self, obj):
        return obj.created_at

    get_created.short_description = 'Ուղարկման օր և ժամ'

    def get_file(self, obj):
        return mark_safe(f'<a href="{obj.cv.url}" target="_blank">{obj.job.name}</a>')

    get_file.short_description = 'Դիտել ֆայլը'


    list_display.insert(1, 'get_file')
    list_display.insert(3, 'get_created')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

class JobItemAdmin(TabbedDjangoJqueryTranslationAdmin):
    list_display = ['id', 'name']

    def get_icon(self, obj: JobItem):
        if obj.icon:
            return mark_safe(f'<img src="{obj.icon.url}" height="100px" width="100px" />')
        return mark_safe(f'<img src="{STATIC_URL}img/icons/job-icon.svg" height="100px" width="100px" />')

    get_icon.short_description = "Նկար"

    list_display.insert(1, 'get_icon')


admin.site.register(JobItem, JobItemAdmin)

class CustomResumeForJobAdmin(admin.ModelAdmin):

    def get_editor1(self, obj):
        return mark_safe(f'{obj.editor1}')

    def get_editor2(self, obj):
        return mark_safe(f'{obj.editor2}')

    def get_editor3(self, obj):
        return mark_safe(f'{obj.editor3}')

    def get_editor4(self, obj):
        return mark_safe(f'{obj.editor4}')

    def get_editor5(self, obj):
        return mark_safe(f'{obj.editor5}')

    def get_edito6(self, obj):
        return mark_safe(f'{obj.edito6}')

    get_editor1.short_description='Մասնագիտական փորձ'
    get_editor2.short_description='Կրթություն և դասընթաց'
    get_editor3.short_description='Մասնագիտական հմտություններ'
    get_editor4.short_description='Անձնական հմտություններ'
    get_editor5.short_description='Լեզուներ'
    get_edito6.short_description='Այլ տեղեկություններ'

    fields = ['job', 'avatar', 'name', 'gender', 'birthday', 'email', 'address', 'phone']
    readonly_fields = ['get_editor1',
                        'get_editor2',
                        'get_editor3',
                        'get_editor4',
                        'get_editor5',
                        'get_edito6',
                       ]

    fields.extend(readonly_fields)
admin.site.register(CustomResumeForJob, CustomResumeForJobAdmin)