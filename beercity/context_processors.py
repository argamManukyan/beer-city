""" Here are global context processors, which apply to the app """

from threading import Thread
from typing import List, Any

from currencies.models import Currency
from django.conf import settings
from django.urls import reverse
from aboutus.models import Partners

from footer.models import *
from header.models import *
from shop.models import Category, BonusDays, CategoryBonuses
from users.models import User
from flatpages.models import ContactUs, ContactUsPageIframe


class RemoveCategoryBonusDays(Thread):
    def __init__(self, bday_pk: int):
        self.bday_pk = bday_pk
        Thread.__init__(self)

    def run(self) -> None:
        CategoryBonuses.objects.filter(bonus_id=self.bday_pk).delete()


def partners(request):
    """ Return all partners list """

    if 'currency' not in request.session:
        request.session['currency'] = settings.CURRENCY
        request.session['currency_icon'] = Currency.objects.get(code__icontains=settings.CURRENCY).symbol

    return {"partners": Partners.objects.all()}


def informative_links(request):
    """ Return all informative datas """
    return {"informative_links": PersonalData.objects.all()}


def delete_user(request):
    """ Delete the user which not set password """
    if request.resolver_match.url_name != "set_password" and \
            request.META.get('HTTP_REFERER') and request.META.get('HTTP_REFERER') \
            == request.build_absolute_uri(reverse('users:set_password')):
        if 'phone_number' in request.session:
            User.objects.filter(phone_number=request.session.get('phone_number')).delete()
            del request.session['phone_number']
    return []


def footer_categories(request):
    """ Get all footer categories with select_related """
    return {"footer_categories": FooterCategory.objects.prefetch_related('items').distinct()}


def social_buttons(request):
    """ Return all social share icons """
    return {"social_buttons": SocialIcons.objects.all()}


def contact_us_page_iframe(request):
    return {"iframe": ContactUsPageIframe.objects.first()}


def bank_icons(request):
    """ Bank icons list """
    return {"bank_icons": BankIcons.objects.all()}


def get_year(request):
    """ Get current year, for footer corporate """
    from datetime import datetime

    return {"get_year": datetime.today().year}


def get_site(request):
    """ Return site domain """
    from django.contrib.sites.shortcuts import get_current_site

    full_link = 'http://' if not request.is_secure() else 'https://'
    full_link += get_current_site(request).domain
    return {"site": full_link}


def to_header_items(request):
    """ Return all top header items """

    return {"to_header_items": TopHeader.objects.all()[:2]}


def to_header_items_two(request):
    """ Return all top header items """
    if TopHeader.objects.count() > 2:
        return {"to_header_items_two": TopHeader.objects.all()[2:]}
    return {"to_header_items_two": []}


def bottom_header_items(request):
    """ Return all bottom header items """

    return {"bottom_header_items": BottomHeader.objects.all()}


def header_categories(request):
    """ Return all categories which are selected for show on header """

    return {"header_categories": Category.objects.filter(show_in_header=True)}


def check_bonus_day_actuality(request) -> List[Any]:
    """ Check and change status of bonus day active or inactive, and delete all of them categoryBonuses """

    from django.utils import timezone

    active_bonus_days = BonusDays.objects.filter(is_active=True)
    if active_bonus_days.count():
        if active_bonus_days.filter(active_from__lt=timezone.now()).exists():
            for i in active_bonus_days:
                i.is_active = False
                i.save()
                RemoveCategoryBonusDays(i.pk).start()

    return []


def get_domain(request):
    """ Method for return domain for meta titles if meta title some model instances can be empty """

    from django.contrib.sites.shortcuts import get_current_site

    return {"domain": get_current_site(request).domain.capitalize()}
