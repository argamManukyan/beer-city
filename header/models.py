from django.db import models
from canapea.utils import CustomLogoField


class TopHeader(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name='Դաշտի անուն')
    url = models.URLField(verbose_name='Հղում')
    icon = CustomLogoField()
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['my_order']


class BottomHeader(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name='Դաշտի անուն')
    url = models.URLField(verbose_name='Հղում')
    # icon = CustomLogoField()
    with_underscore = models.BooleanField(
        default=False,
        help_text='Այս դաշտը հնարավորություն է տալիս գծանշել դաշտը',
        verbose_name='Գծանշել'
    )
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['my_order']