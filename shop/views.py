import json
from decimal import Decimal

import requests
from currencies.models import Currency
from currencies.utils import calculate
from django.db.models import Min, Max, Q, Avg, Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from breadcrumbs.models import BreadcrumbTexts
from videos.models import Video

FURSHET_SLUG = settings.FURSHET_CATEGORY_SLUG_NAME
MENU_SLUG = settings.MENU_CATEGORY_SLUG_NAME

from .mixins import ShopMixin
from .models import *


@csrf_exempt
def setcurrency(request):
    """ Change currency view """
    import xmltodict

    last_link = request.META['HTTP_REFERER']
    url = "http://api.cba.am/exchangerates.asmx?op=ExchangeRatesLatest"
    headers = {'Content-Type': 'text/xml; charset=utf-8'}
    body = """<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                    <ExchangeRatesLatest xmlns="http://www.cba.am/" />
                </soap:Body>
                </soap:Envelope>
                """

    response = requests.post(url, data=body, headers=headers)
    dict_data = xmltodict.parse(response.content)
    json_data = json.dumps(dict_data, indent=2)
    data = json.loads(json_data)
    rates = data['soap:Envelope']['soap:Body']['ExchangeRatesLatestResponse']['ExchangeRatesLatestResult']['Rates'][
        'ExchangeRate']

    usd = None
    rub = None
    eur = None
    for i in rates:
        if i['ISO'] == 'USD':
            usd = i['Rate']
        elif i['ISO'] == 'EUR':
            eur = i['Rate']
        elif i['ISO'] == 'RUB':
            rub = i['Rate']

    for c in Currency.objects.all():
        if c.code == 'AMD':
            c.factor = 1
            c.save()
        elif c.code == 'USD':
            c.factor = float(1 / Decimal(usd))
            c.save()
        elif c.code == 'EUR':
            c.factor = float(1 / Decimal(eur))
            c.save()
        elif c.code == 'RUB':
            c.factor = float(1 / Decimal(rub))
            c.save()

    if request.method == 'POST':
        request.session['currency'] = request.POST['currency']
        request.session['currency_icon'] = Currency.objects.get(code__icontains=request.POST['currency']).symbol
        return HttpResponseRedirect(last_link)
    return HttpResponseRedirect(last_link)


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class HomePageView(View):
    """ Home page """

    def get(self, request, **kwargs):
        used_ids = []
        slider = Slider.objects.all()
        special_offers = Product.objects.filter(special_offer=True)[:16]
        used_ids.append(special_offers.values_list('id', flat=True))
        best_sold_furshets = Product.objects.filter(
            category__slug=FURSHET_SLUG)
        used_ids.append(best_sold_furshets.values_list('id', flat=True))

        banners = HomepageBanners.objects.all()
        homepage_categories = Category.objects.filter(parent=None, show_homepage=True).distinct()
        bullets = Bullets.objects.all()
        video_and_text = Video.objects.filter(location='home').first()
        show_products_homepage = Category.objects.filter(show_homepage_products=True).distinct()
        products = Product.objects.all()
        context = {
            "slider": slider,
            "special_offers": special_offers,
            "best_sold_furshets": best_sold_furshets,
            "banners": banners,
            "homepage_categories": homepage_categories,
            "show_products_homepage": show_products_homepage,
            "bullets": bullets,
            "used_ids": used_ids,
            "products": products,
            "video_and_text": video_and_text,
        }
        return render(request, 'shop/index.html', context)


class CategoryDetailView(ShopMixin):
    """ Category page """

    def get(self, request, **kwargs):
        category = get_object_or_404(Category, slug=kwargs['slug'])

        list_id_category = [i.id for i in category.get_descendants(include_self=True).filter(is_active=True)]

        category_min_price = Product.objects.filter(
            category__in=list_id_category).aggregate(min_price=Min('finally_price'))['min_price'] or 0
        category_max_price = Product.objects.filter(
            category__in=list_id_category).aggregate(max_price=Max('finally_price'))['max_price'] or 0

        products = Product.objects.filter(category__in=list_id_category).order_by('-id').distinct()
        page_obj = self.filter_products(products)

        filter_fields = FilterField.objects.filter(Q(productfeature__product__category__in=list_id_category) |
                                                   Q(productfeature__product__category__slug=category.slug,
                                                     show_in_filters=True),
                                                   Q(productfeature__value__isnull=False)).distinct()

        featured_values = FilterValue.objects.filter(Q(productfeature__product__category__in=list_id_category) |
                                                     Q(productfeature__product__category__slug=category.slug,
                                                       productfeature__field__show_in_filters=True),
                                                     Q(productfeature__value__isnull=False)).distinct()
        colors = Color.objects.filter(product__category=category).distinct()

        if self.request.is_ajax():
            return self.show_filter_data(products)

        context = {
            "category": category,
            "category_min_price": category_min_price,
            "category_max_price": category_max_price,
            "page_obj": page_obj,
            "filter_fields": filter_fields,
            "featured_values": featured_values,
            "colors": colors,
            "breadcrumbs": category.get_ancestors()
        }
        return render(request, 'shop/shop.html', context)


class ProductDetailView(DetailView):
    model = Product
    queryset = Product.objects.all()
    slug_field = 'slug'
    template_name = 'shop/product_page.html'
    context_object_name = 'obj'

    def add_viewed_list(self):

        if 'recently_views' not in self.request.session:
            self.request.session['recently_views'] = []

        if self.get_object().pk not in self.request.session['recently_views']:
            self.request.session['recently_views'].append(self.get_object().pk)

        return self.request.session['recently_views']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inheritance_items = self.get_object().category.filter(
            show_category_all_items=True).first()

        context['ratings'] = Rating.objects.order_by('-value')
        context['middle_score'] = self.get_object().ratingproduct_set.aggregate(
            middle=Avg('rating__value'))
        context['middle'] = float('{:.1f}'.format(context['middle_score'].get('middle') or 0))
        context['user_block'] = RatingProduct.objects.filter(ip=get_ip(self.request),
                                                             product_id=self.get_object().id).exists()
        context['user_rating'] = None
        if context['user_block']:
            context['user_rating'] = RatingProduct.objects.get(ip=get_ip(self.request),
                                                               product_id=self.get_object().pk)

        if inheritance_items:
            context['inheritance_items'] = sorted(inheritance_items.product_set.all(),
                                                  key=lambda x: x.id == self.get_object().id, reverse=True)
        context['variant_fields'] = FilterField.objects.filter(productfeature__product_id=self.get_object().id,
                                                               is_main=True,
                                                               productfeature__value__isnull=False).distinct()
        context['main_fields'] = self.get_object().productfeature_set.all()
        context['variant_values'] = context['main_fields'].filter(field__is_main=True).order_by('price')

        context['features'] = context['main_fields'].filter(field__is_main=False)
        context['ingredients'] = ProductIngredient.objects.filter(product=self.get_object())
        try:
            latest_visited_cat = self.request.META.get('HTTP_REFERER').split('/')[-2]
            bred_category = Category.objects.get(slug=latest_visited_cat, is_active=True)
        except:
            bred_category = Category.objects.filter(product__slug__iexact=self.get_object().slug,
                                                    is_active=True).first()

        context["breadcrumbs"] = bred_category.get_ancestors(include_self=True)

        # bellow sections
        recently_views = Product.objects.filter(id__in=self.add_viewed_list()).exclude(
            pk=self.get_object().pk).distinct()
        buy_with_this_item = self.get_object().buy_with_this_item.exclude(
            Q(id__in=recently_views.values_list('id', flat=True)) | Q(id=self.get_object().pk)).distinct()
        category_items = Product.objects.filter(
            category__in=self.get_object().category.first().get_family().values_list(
                'id', flat=True)).exclude(
            Q(id__in=recently_views.values_list('id', flat=True)) | Q(id=self.get_object().pk) |
            Q(id__in=buy_with_this_item.values_list('id', flat=True))).distinct()

        context.update({
            'recently_views': recently_views,
            'buy_with_this_item': buy_with_this_item,
            'category_items': category_items[:16],
            'video': Video.objects.filter(Q(video_file__isnull=False) | Q(video_url__isnull=False),
                                          location='product_page').distinct().first()
        })
        return context


@csrf_exempt
def create_rating(request):
    if request.method == 'GET':
        return HttpResponse(status=405, content={"detail": 'Method not allowed'})

    data = json.loads(request.body)
    rating_id = data.get('rating')
    rating_id = Rating.objects.get(value=rating_id)
    product_id = data.get('product')
    try:
        product_rating, _ = RatingProduct.objects.update_or_create(product_id=product_id,
                                                                   ip=get_ip(request),
                                                                   defaults={'rating_id': rating_id.id}
                                                                   )

    except Exception as e:
        return HttpResponse(status=400)

    middle_score = RatingProduct.objects.filter(product_id=product_id).aggregate(middle=Avg('rating__value'))
    middle = float('{:.1f}'.format(middle_score.get('middle')))
    return JsonResponse({'success': 'Rating created', 'rating': middle})


class CreateSubscriptionView(View):

    def post(self, request, **kwargs):
        email = request.POST.get('email')

        if email and not Subscriptions.objects.filter(email=email).exists():
            Subscriptions.objects.create(email=email)

        last_link = request.META['HTTP_REFERER']

        return HttpResponseRedirect(last_link)


class MenuView(View):

    def get(self, request, **kwargs):
        menu = get_object_or_404(Category, slug=MENU_SLUG)
        childs = menu.get_descendants(include_self=False)
        context = {'menu': menu, 'childs': childs}
        return render(request, 'shop/menu.html', context)


class CatalogView(View):

    def get(self, request, **kwargs):
        main_categories = Category.objects.filter(parent=None)
        st_content = BreadcrumbTexts.objects.filter(location='catalog').first()
        context = {
            'main_categories': main_categories,
            'st_content': st_content
        }

        # TODO: add breadcrumb text and image
        return render(request, 'shop/catalog.html', context)


class SaleOfferNewBestSellerView(ShopMixin):

    def get_queryset(self, products):

        query_param = self.request.GET.get('type')
        if query_param == 'new':
            products = products.order_by('-id')
        if query_param == 'sale':
            products = products.filter(sale__gt=0)
        if query_param == 'best_seller':
            products = products.filter(best_seller=True)
        if query_param == 'special_offer':
            products = products.filter(special_offer=True)
        else:
            products = products.order_by('-id')

        return products

    def get(self, request, **kwargs):
        products = self.get_queryset(Product.objects.filter(is_active=True))
        category_min_price = products.aggregate(min_price=Min('finally_price'))['min_price'] or 0
        category_max_price = products.aggregate(max_price=Max('finally_price'))['max_price'] or 0

        filter_fields = FilterField.objects.filter(Q(productfeature__value__isnull=False)).distinct()

        featured_values = FilterValue.objects.filter(productfeature__field__show_in_filters=True,
                                                     productfeature__value__isnull=False).distinct()
        colors = Color.objects.distinct()

        if self.request.is_ajax():
            return self.show_filter_data(products)

        context = {
            'page_obj': self.paginate_queryset(products),
            'filter_fields': filter_fields,
            'featured_values': featured_values,
            'colors': colors,

        }

        if request.GET.get('type') in ['new', 'sale', 'best_seller', 'special_offer']:
            if request.GET.get('type') == 'new' or not request.GET.get('type'):
                st_content = BreadcrumbTexts.objects.filter(location='new').first()
                context['st_content'] = st_content
            if request.GET.get('type') == 'sale':
                st_content = BreadcrumbTexts.objects.filter(location='sale').first()
                context['st_content'] = st_content
            if request.GET.get('type') == 'best_seller':
                st_content = BreadcrumbTexts.objects.filter(location='best_seller').first()
                context['st_content'] = st_content
            if request.GET.get('type') == 'special_offer':
                st_content = BreadcrumbTexts.objects.filter(location='special_offer').first()
                context['st_content'] = st_content

            context.update({
                "category_min_price": category_min_price,
                "category_max_price": category_max_price,
                "categories": Category.objects.filter(parent=None)

            })
            return render(request, 'shop/sale_offer.html', context)

        return redirect(reverse('offers') + '?type=new')


class SearchView(ShopMixin):

    def get(self, request, **kwargs):

        q = request.GET.get('q')
        products = Product.objects.all()
        if q:
            products = products.filter(Q(name__icontains=q) | Q(slug__icontains=q))
        page_obj = self.filter_products(products)

        category_min_price = products.aggregate(min_price=Min('finally_price'))['min_price'] or 0
        category_max_price = products.aggregate(max_price=Max('finally_price'))['max_price'] or 0

        filter_fields = FilterField.objects.filter(productfeature__value__isnull=False).distinct()
        featured_values = FilterValue.objects.filter(productfeature__field__show_in_filters=True,
                                                     productfeature__value__isnull=False).distinct()
        colors = Color.objects.distinct()

        if self.request.is_ajax():
            return self.show_filter_data(products)

        context = {
            "page_obj": page_obj,
            "category_min_price": category_min_price,
            "category_max_price": category_max_price,
            "categories": Category.objects.filter(parent=None),
            "filter_fields": filter_fields,
            "featured_values": featured_values,
            "colors": colors,
        }
        if q and q.isalpha():
            context.update({'q': q})
        st_content = BreadcrumbTexts.objects.filter(location='search').first()
        context['st_content'] = st_content

        return render(request, 'shop/search.html', context)


def ajaxSearch(request):
    data = request.GET.get('q')

    return_dict = dict()
    return_dict['products'] = list()
    if data or data == "":
        products = Product.objects.filter(Q(name__icontains=data) | Q(slug__icontains=data) |
                                          Q(product_code__contains=data)).distinct().order_by('?')[:15]
        for product in products:
            new_dict = dict()
            new_dict['name'] = product.name
            new_dict['image'] = product.main_image.url
            new_dict['slug'] = product.get_absolute_url()

            return_dict['products'].append(new_dict)

    return JsonResponse(return_dict)


def change_qty(request, pk):
    product = Product.objects.get(pk=pk)
    items = {k: v for k, v in request.GET.items() if k != "qty" and v != ""}
    values = list(items.values())
    qty = int(request.GET.get('qty'))
    items_total = ProductFeature.objects.filter(id__in=values).aggregate(sum=Sum("price"))['sum'] or 0

    if product.sale:
        return JsonResponse(
            {
                "price": "{:,}".format(qty * calculate(product.price + items_total, request.session.get('currency'))),
                "sale": "{:,}".format(qty * calculate(product.sale + items_total, request.session.get('currency'))),
                "obj_price": "{:,}".format(calculate(product.price, request.session.get('currency'))),
                "obj_sale": "{:,}".format(calculate(product.sale, request.session.get('currency')))
             })
    return JsonResponse(
        {
            "price": "{:,}".format(qty * calculate(product.price + items_total, request.session.get('currency'))),
            "obj_price": "{:,}".format(calculate(product.price, request.session.get('currency'))),
        })
