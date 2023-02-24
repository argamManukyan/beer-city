from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse

from beercity.utils import CustomMetaModel, slug_generator, CustomLogoField, CustomModel


class FlatPages(CustomMetaModel):
    page_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = RichTextUploadingField()

    def __str__(self):
        return self.page_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_generator(self.page_name)

        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ստատիկ էջ'
        verbose_name_plural = 'Ստատիկ էջեր'


class BlogCategory(CustomMetaModel):
    name = models.CharField(max_length=255, verbose_name="Բաժնի անուն")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="Հղում")
    breadcrumb_image = CustomLogoField(verbose_name='Բաժնի բանների նկար',
                                       blank=True, null=True, upload_to='blog-cat-bg-image/')
    breadcrumb_text = RichTextUploadingField(verbose_name="Բանների տեքստ", blank=True, null=True)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-my_order']
        verbose_name = "Բլոգի բաժին"
        verbose_name_plural = "Բլոգի բաժիններ"

    def get_absolute_url(self):
        return reverse('blog_category', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_generator(self.name)

        return super().save(*args, **kwargs)


class Blog(CustomMetaModel):
    category = models.ForeignKey(BlogCategory,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 verbose_name="Ընտրել բաժինը")
    name = models.CharField(max_length=255, verbose_name="Վերնագիր")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="Հղում")
    short_text = RichTextUploadingField(verbose_name="Հակիրճ տեքստ", blank=True, null=True)
    large_text = RichTextUploadingField(verbose_name="Ամբողջական տեքստ")
    views_count = models.PositiveIntegerField(default=0, editable=False)
    image = CustomLogoField(verbose_name='Գլխավոր նկար', blank=True, null=True, upload_to='blog-image/')
    my_order = models.PositiveIntegerField(default=0, verbose_name="Դասավորել")

    class Meta:
        ordering = ['-my_order']
        verbose_name = "Բլոգ"
        verbose_name_plural = 'Բլոգ'

    @property
    def likes_count(self):
        return self.bloglike_set.count()

    def get_absolute_url(self):
        return reverse('blog_details', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_generator(self.name)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogLike(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    device = models.CharField(max_length=255)


class GalleryCategory(CustomMetaModel):
    name = models.CharField(max_length=255, verbose_name="Բաժնի անուն")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="Հղում")
    my_order = models.PositiveIntegerField(default=0, verbose_name="Դասավորել")
    breadcrumbs_image = CustomLogoField(verbose_name='Բաժնի բանների նկար', blank=True, null=True,
                                        upload_to='gallery-category-bg/')
    breadcrumb_text = RichTextUploadingField(verbose_name="Բանների տեքստ", blank=True, null=True,)

    def get_absolute_url(self):
        return reverse('gallery_details', kwargs={"slug": self.slug})

    class Meta:
        ordering = ['-my_order']
        verbose_name = "Տեսադարանի բաժին"
        verbose_name_plural = "Տեսադարանի բաժիններ"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_generator(self.name)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Gallery(CustomModel):
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL,
                                 null=True, blank=True, verbose_name="Ընտրել բաժինը")
    image = CustomLogoField(upload_to='gallery/')
    my_order = models.PositiveIntegerField(default=0, verbose_name="Դասավորել")

    class Meta:
        ordering = ['-my_order']
        verbose_name = "Նկար"
        verbose_name_plural = "Տեսադարան"
        

class FAQModel(CustomModel):
    question = RichTextUploadingField(verbose_name="Հարց", max_length=500)
    answer = RichTextUploadingField(verbose_name="Պատասխան", max_length=500)
    my_order = models.PositiveIntegerField(verbose_name="Դասավորել", default=0)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['-my_order']
        verbose_name = "Հաճախակի տրվող հարց"
        verbose_name_plural = "Հաճախակի տրվող հարցեր"