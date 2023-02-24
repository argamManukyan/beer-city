from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin
from adminsortable2.admin import SortableAdminMixin
from .models import *

admin.site.register(FlatPages, TabbedDjangoJqueryTranslationAdmin)


class GalleryUploadForm(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Gallery
        fields = "__all__"


@admin.register(BlogCategory)
class BlogCategoryAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(Blog)
class BlogAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    list_display = ['name']

    def get_image(self, obj):
        if obj.image:
            return mark_safe("<img src='{}' height='100px' width='100px' />".format(obj.image.url))

    get_image.short_description = 'Նկար'
    list_display.append('get_image')


@admin.register(Gallery)
class GalleryImagesAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = GalleryUploadForm

    def save_model(self, request, obj, form, change):
        obj.save()
        img_list = request.FILES.getlist('image')[:-1]
        for i in img_list:
            Gallery.objects.create(category_id=obj.category.id, image=i)

    def image_tag(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="width:150px;height:150px;margin-right:10px" /> ')

    image_tag.short_description = 'Image'

    list_display = ['image_tag', 'category']


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass


@admin.register(FAQModel)
class FAQModelAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin):
    pass