from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import *


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'verification_code',
                                        'city', 'state', 'phone_number')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'birthday')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget
from import_export import fields


class StateResource(ModelResource):
    state = fields.Field(attribute='state', column_name='state', widget=ForeignKeyWidget(State, 'name_hy'))

    class Meta:
        model = Country


class ExcellModelImport(ImportExportModelAdmin):
    resource_class = StateResource


class GenericModelField(ExcellModelImport):
    search_fields = ['name']


admin.site.register(State, ImportExportModelAdmin)
admin.site.register(Country, GenericModelField)
