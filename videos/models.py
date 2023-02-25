from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


class Video(models.Model):
    LOCATION_OF_VIDEO = [
        ('home', 'Գլխավոր էջ'),
    ]

    location = models.CharField(
        max_length=100,
        choices=LOCATION_OF_VIDEO,
        default=LOCATION_OF_VIDEO[0][0],
        verbose_name="Ընտրեք էջը"
    )
    video_url = models.URLField(verbose_name='Տեսահոլովակի հղում', blank=True)
    video_file = models.FileField(verbose_name='Տեսահոլովակ', blank=True)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')
    text = RichTextUploadingField(blank=True, null=True, verbose_name="Տեքստ")

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Տեսահոլովակ'
        verbose_name_plural = 'Տեսահոլովակ'
        ordering = ['my_order']


