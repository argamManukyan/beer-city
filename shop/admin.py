import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from singlemodeladmin import SingleModelAdmin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from mptt.admin import DraggableMPTTAdmin
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin
from easy_select2 import select2_modelform


from .models import *

admin.site.site_header = 'Beer city'                    # default: "Django Administration"
admin.site.index_title = 'Beer city'                 # default: "Site administration"
admin.site.site_title = 'Beer city'

ProductForm = select2_modelform(Product,  attrs={"width": "250px"})


class ProductImageInlineAdmin(SortableInlineAdminMixin, admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductFeatureInlineAdmin(SortableInlineAdminMixin, admin.TabularInline):
    model = ProductFeature
    extra = 0
    form = select2_modelform(model,  attrs={"width": "250px"})


class ProductIngredientInlineAdmin(SortableInlineAdminMixin, admin.TabularInline):
    model = ProductIngredient
    extra = 0
    form = select2_modelform(model,  attrs={"width": "250px"})


def set_meta_fields_before_form(resp):
    """ custom method for moving meta fields """

    meta_title = resp.pop(0)
    meta_description = resp.pop(0)
    resp += [str(meta_title)]
    resp += [str(meta_description)]

    return resp



@admin.register(Slider)
class SliderAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):

    def get_xl_image(self, instance: Slider):
        if instance.xl_image:
            return mark_safe('<img src="{}" height="120px" width="120px" />'.format(instance.xl_image.url))

    def get_lg_image(self, instance: Slider):
        if instance.lg_image:
            return mark_safe('<img src="{}" height="120px" width="320px" />'.format(instance.lg_image.url))

    get_xl_image.short_description = 'Mobile Նկար'
    get_lg_image.short_description = 'Desktop Նկար'

    list_display = ['get_xl_image', 'get_lg_image']


@admin.register(Category)
class CategoryAdmin(TabbedDjangoJqueryTranslationAdmin, DraggableMPTTAdmin):
    exclude = ['large_description']
    form = select2_modelform(Category, attrs={"width": "250px"})

    def get_fields(self, request, obj=None):
        resp = super().get_fields(request, obj)
        if 'meta_title' in resp:
            return set_meta_fields_before_form(resp)
        return resp


#     # fieldsets = [
#     #     (None, {
#     #         'fields': ('parent', 'name', 'slug', 'show_in_header',
#     #                    'homepage_name', 'breadcrumb_image', 'short_description',
#     #                    'show_homepage', 'homepage_qty', 'sub_title_color', 'color',
#     #
#     #                    )
#     #     }),
#     # ]
#         # ('Advanced options', {
#         #     'classes': ('collapse',),
#         #     'fields': ('registration_required', 'template_name'),
#         # }),
#     # ]
#

class ProductAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    inlines = [ProductFeatureInlineAdmin, ProductImageInlineAdmin, ProductIngredientInlineAdmin]
    form = ProductForm
    list_filter = ['category']
    search_fields = ['name', 'product_code', 'name_ru', 'name_en']

    def get_image(self, obj):
        if obj.main_image:
            return mark_safe('<img src="{}" height="200px" width="200px" />'.format(obj.main_image.url))

    get_image.short_description = "Նկար"
    list_display = ['get_image', 'name', 'price', 'sale',  'product_code']


admin.site.register(Product, ProductAdmin)
admin.site.register(Ingredient)


@admin.register(Color)
class ColorModelAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(HomepageBanners)
class HomepageBannersModelAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(FilterField)
class FilterFieldModelAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(Bullets)
class BulletsModelAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(Subscriptions)
class SubscriptionsModelAdmin(admin.ModelAdmin):

    list_display = ['email', 'created_at']

    def download_csv(self, request, queryset):
        response = HttpResponse('text/csv')
        response['Content-Disposition'] = 'attachment; filename=subscribers.csv'
        writer = csv.writer(response)
        writer.writerow(['email', 'created_at'])
        studs = queryset.values_list('email', 'created_at')
        for std in studs:
            writer.writerow(std)
        return response

    actions = [download_csv]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False




@admin.register(FilterValue)
class FilterValueModelAdmin(TabbedDjangoJqueryTranslationAdmin):
    pass


admin.site.register(Rating)
admin.site.register(RatingProduct)
# admin.site.register(ProductFeature)
admin.site.register(UnitMeasurement, TabbedDjangoJqueryTranslationAdmin)

admin.site.register(SliderPhoneImage, SingleModelAdmin)