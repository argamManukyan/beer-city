from django.db import models
from beercity.utils import CustomModel, CustomLogoField


TEXT_LOCATION = [
    ('catalog', 'Տեսականի'),
    ('sale', 'Ակցիա'),
    ('new', 'Նորույթ'),
    ('best_seller', 'Բեսթսելլեր'),
    ('special_offer', 'Հատուկ առաջարկ'),
    ('search', 'Որոնում'),
    ('blog', 'Բլոգ'),
    ('gallery', 'Տեսադարան'),
    ('contacts', 'Կապ'),
    ('abouts', 'Մեր մասին'),
    ('job', "Աշխատանք")
]


class BreadcrumbTexts(CustomModel):
    """ Breadcrumb texts and images """
    location = models.CharField(choices=TEXT_LOCATION, max_length=150, unique=True, verbose_name='Ընտրեք էջը')
    breadcrumbs_text = models.TextField(blank=True, null=True, verbose_name='Breadcrumb -ի տեքստ')
    breadcrumbs_image = CustomLogoField(blank=True, null=True, verbose_name='Breadcrumb -ի Նկար')
    page_title = models.CharField(max_length=255, blank=True, verbose_name='Էջի վերնագիր')

    def __str__(self):
        return f'{self.page_title}'

    class Meta:
        verbose_name = 'Breadcrumb -ի կոնտենտ'
        verbose_name_plural = verbose_name
