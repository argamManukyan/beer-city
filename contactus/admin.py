from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from modeltranslation.admin import TranslationInlineModelAdmin, TabbedDjangoJqueryTranslationAdmin
from singlemodeladmin import SingleModelAdmin

from contactus.models import ContactUs, ContactUsPage, FollowUsContactUs, ContactUsJoinUsData


class TabulaInlineContactJoinUs(SortableInlineAdminMixin, TranslationInlineModelAdmin, admin.StackedInline):
    model = ContactUsJoinUsData
    extra = 0


class TabulaInlineContactFollow(SortableInlineAdminMixin, TranslationInlineModelAdmin, admin.StackedInline):
    model = FollowUsContactUs
    extra = 0


@admin.register(ContactUsPage)
class ContactUsPageModelAdmin(SingleModelAdmin, TabbedDjangoJqueryTranslationAdmin):
    inlines = [TabulaInlineContactJoinUs, TabulaInlineContactFollow]


@admin.register(ContactUs)
class ContactUsRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'created_at']
