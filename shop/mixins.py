import datetime

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View

from shop.models import Category


class ShopMixin(View):
    PAGE_SIZE = 12

    def generate_link(self):
        return self.request.GET.urlencode()

    def get_parents(self):
        return Category.objects.filter(parent=None)

    def show_filter_data(self, products):
        data = {
            "link": self.generate_link(),
            "products": render_to_string('includes/filter_product.html', context={
                "page_obj": self.filter_products(products),
            }, request=self.request)
        }

        return JsonResponse(data)

    def paginate_queryset(self, products):
        page = self.request.GET.get('page')
        paginator = Paginator(products, self.PAGE_SIZE)
        return paginator.get_page(page)

    def filter_products(self, products) -> list:
        url_kwargs = {}
        request = self.request
        for item in request.GET:
            if len(request.GET.getlist(item)) > 1:
                url_kwargs[item] = request.GET.getlist(item)
            else:
                url_kwargs[item] = request.GET.get(item)
        q_condition_queries = []

        for key, value in url_kwargs.items():
            if key not in ['min_price', 'max_price', 'page', 'sorting', 'top_filter', 'type', 'q']:
                if isinstance(value, list):
                    if key == 'color':
                        q_condition_queries.append(
                            {'color__title__in': value})
                    elif key == 'brand':
                        q_condition_queries.append(
                            {'brand__name__in': value}
                        )
                    else:
                        q_condition_queries.append(
                            {f'productfeature__field__filter_key': key, 'productfeature__value__title__in': value})
                else:
                    if key == 'color':
                        q_condition_queries.append(
                            {'color__title': value})
                    elif key == 'brand':
                        q_condition_queries.append(
                            {'brand__name': value}
                        )
                    else:
                        q_condition_queries.append(
                            {f'productfeature__value__title': value, 'productfeature__field__filter_key': key})

        if request.GET.get('min_price'):
            products = products.filter(finally_price__gte=int(request.GET.get('min_price')))
        if request.GET.get('max_price'):
            products = products.filter(finally_price__lte=int(request.GET.get('max_price')))

        if request.GET.getlist('top_filter'):
            for t_fil in request.GET.getlist('top_filter'):
                if t_fil == 'new':
                    products = products.filter(created_at__gte=(timezone.now() - datetime.timedelta(days=15)))
                if t_fil == 'sale':
                    products = products.filter(sale__gt=1)
                if t_fil == 'special_offer':
                    products = products.filter(special_offer=True)
                if t_fil == 'best_seller':
                    products = products.filter(best_seller=True)

        if len(q_condition_queries):
            for filter_item in q_condition_queries:
                products = products.filter(**filter_item).distinct()
        if request.GET.get('sorting'):
            products = products.order_by(request.GET.get('sorting'))
        else:
            products = products.order_by('-id')

        return self.paginate_queryset(products)
