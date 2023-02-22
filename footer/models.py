from django.db import models

from beercity.utils import CustomLogoField


class FooterCategory(models.Model):
    title = models.CharField(max_length=255, unique=True)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Footer -ի բաժին'
        verbose_name_plural = 'Footer -ի բաժիններ'


class Footer(models.Model):

    LOGIN_CHOICES = [
        ('logged', 'Օգտատերեր'),
        ('guests', 'Հյուրեր'),
    ]

    category = models.ForeignKey(FooterCategory, on_delete=models.PROTECT,
                                 verbose_name='Բաժնի անուն', related_name='items')
    title = models.CharField(max_length=255, unique=True, verbose_name='Դաշտի անուն')
    url = models.URLField(verbose_name='Հղում')
    is_logged = models.CharField(help_text='Դաշտի հասանելիության տիրույթ, դաշտի դատարկ լինելու'
                                           ' դեպքում այն տեսանելի կլինի բոլորին', blank=True, null=True,
                                 verbose_name='Ցուցադրման տիրույթ', choices=LOGIN_CHOICES, max_length=120)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['my_order']


class SocialIcons(models.Model):
    url = models.URLField(verbose_name='Հղում')
    icon = CustomLogoField()
    title = models.CharField(max_length=255, unique=True, verbose_name='Անուն (alt)')
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Սոց ցանցի լոգո'
        verbose_name_plural = 'Սոց ցանցերի լոգոներ'


class BankIcons(models.Model):
    url = models.URLField(verbose_name='Հղում', blank=True, null=True)
    icon = CustomLogoField()
    title = models.CharField(max_length=255, unique=True, verbose_name='Անուն (alt)')
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Բանկի լոգո'
        verbose_name_plural = 'Բանկերի լոգոներ'


class PersonalData(models.Model):
    """ Company personal data """
    icon = CustomLogoField(blank=True)
    text = models.CharField(max_length=255, verbose_name='Տեքստ')
    url = models.CharField(max_length=255, blank=True, null=True, verbose_name='Հղում')
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name='Դասավորել')

    class Meta:
        ordering = ['my_order']
        verbose_name = 'Ընկերության տվյալ'
        verbose_name_plural = 'Ընկերության տվյալներ'

    def __str__(self):
        return self.text