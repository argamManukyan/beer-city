import textwrap

from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import FileExtensionValidator
from django.db import models
from beercity.utils import CustomModel, CustomLogoField


class OurGoals(CustomModel):
    my_order = models.PositiveIntegerField(verbose_name="Դասավորել", default=0)
    name = models.CharField(max_length=255, verbose_name="Նպատակի անուն")
    text = models.TextField(verbose_name="Նկարագրություն", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-my_order']
        verbose_name = "Նպատակ"
        verbose_name_plural = "Մեր նպատակները"


class OurAdvantages(CustomModel):
    my_order = models.PositiveIntegerField(verbose_name="Դասավորել", default=0)
    icon = CustomLogoField(blank=True)
    name = models.CharField(max_length=255, verbose_name="Նպատակի անուն")
    text = models.TextField(verbose_name="Նկարագրություն", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-my_order']
        verbose_name = "Առավելություն"
        verbose_name_plural = "Մեր առավելությունները"


class Reviews(CustomModel):
    image = CustomLogoField()
    name = models.CharField(verbose_name="Անուն և ազգանուն", max_length=230)
    text = models.TextField(verbose_name="Կարծիք")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Կարծիք'
        verbose_name_plural = '«Մեր մասին» էջի կարծիքներ'


class GoalImage(models.Model):
    image = CustomLogoField()

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = "«Մեր նպատակները» հատվածի նկար"


class AboutUs(CustomModel):
    file = models.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['flv', 'mp4', 'svg', 'jpg', 'png'])],
        verbose_name="Մեր մասին -ի նկար կամ հոլովակ", blank=True)
    url = models.URLField(verbose_name="Հոլովակի հղում", blank=True, null=True)
    text = RichTextUploadingField()

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = 'Մեր մասին'


class Partners(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Անուն (alt)')
    icon = CustomLogoField()
    url = models.URLField(null=True, blank=True, verbose_name='Հղում դեպի գործընկերոջ կայքէջ')
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Գործընկեր'
        verbose_name_plural = 'Գործընկերներ'

    def __str__(self):
        return self.name if self.name else str(self.pk)
