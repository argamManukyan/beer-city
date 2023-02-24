from django.core.validators import FileExtensionValidator
from django.db import models
from beercity.utils import CustomModel


class ContactUsPage(models.Model):
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(max_length=300, blank=True, null=True)
    iframe = models.TextField(verbose_name="Քարտեզ (Iframe)", blank=True, null=True)
    contact_bg_image = models.FileField(validators=[FileExtensionValidator(
        allowed_extensions=['jpg', 'svg', 'png', 'jpeg', 'webp']
    )], verbose_name="Background -ի Նկար", blank=True, null=True)

    class Meta:
        verbose_name = 'Հետադարձ կապի էջ'
        verbose_name_plural = 'Հետադարձ կապի էջ'
        # ordering = ['-my_order']

    def __str__(self):
        return "Հետադարձ կապի էջի"


class ContactUsJoinUsData(CustomModel):
    contact_us = models.ForeignKey(ContactUsPage, on_delete=models.CASCADE, related_name='contact_icons')
    text = models.CharField(max_length=400, verbose_name="Տեքստ")
    icon = models.FileField(validators=[FileExtensionValidator(
        allowed_extensions=['jpg', 'svg', 'png', 'jpeg']
    )], verbose_name="Նկար", blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True, verbose_name="Հղում")
    phone_url = models.CharField(max_length=500, blank=True, null=True, verbose_name="Mobile -ի Հղում")
    my_order = models.PositiveIntegerField(default=0, verbose_name="Դասավորել")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Կոնտակտային տվյալ"
        verbose_name_plural = "Կոնտակտային տվյալներ"
        ordering = ['-my_order']
        

class FollowUsContactUs(models.Model):
    contact_us = models.ForeignKey(ContactUsPage, on_delete=models.CASCADE, related_name='social_buttons')
    text = models.CharField(max_length=400, verbose_name="Սոց. ցանցի անուն")
    icon = models.FileField(validators=[FileExtensionValidator(
        allowed_extensions=['jpg', 'svg', 'png', 'jpeg']
    )], verbose_name="Նկար")
    link = models.CharField(max_length=500, blank=True, null=True, verbose_name="Հղում")
    my_order = models.PositiveIntegerField(default=0, verbose_name="Դասավորել")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Հետևեք մեզ - սոց. ցանցեր"
        verbose_name_plural = "Հետևեք մեզ - սոց. ցանցեր"
        ordering = ['-my_order']


class ContactUs(CustomModel):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Հետադարձ կապ"
        verbose_name_plural = "Հետադարձ կապ"
