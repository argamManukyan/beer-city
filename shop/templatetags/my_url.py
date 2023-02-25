import decimal
from currencies.templatetags import currency as cr
from django.template import Library
from django.template.defaultfilters import floatformat
from django.http import JsonResponse
from shop.models import Product, Category, ProductFeature, FilterValue
from beercity.utils import current_request

register = Library()


@register.simple_tag
def my_url(value, field, urlencode=None):
    url = '?{}={}'.format(field, value)

    if urlencode:
        querystring = urlencode.split('&')

        filtered_queryset = filter(lambda p: p.split('=')[0] != field, querystring)
        encode_qs = '&'.join(filtered_queryset)
        if encode_qs:
            url += '&{}'.format(encode_qs)
    return url


@register.filter
def exists(qs, parameter):
    list_ids = [i for i in qs.values_list('id', flat=True)]
    return parameter in list_ids


@register.filter(name="cardfilter")
def filter_prod_card_values(qs):
    """ Filter and get list of properties on the product card """
    qs = qs.filter(show_on_product_block=True)

    return qs[:2]


@register.filter(name='returnbonusday')
def returnbonusday(qs):
    qs = qs.filter(bonus_days__isnull=False).first()
    return qs


@register.filter(name='unique')
def unique(qs):
    req = current_request()

    try:
        cat_slug = req.resolver_match.kwargs.get('slug')
        category = Category.objects.get(slug__iexact=cat_slug)
        if category.is_leaf_node():
            list_ids = [category.id]
        else:
            list_ids = [i.id for i in category.get_descendants(include_self=True)]
        qs = qs.filter(product__category__in=list_ids)
    except Category.DoesNotExist:
        qs = qs.all()

    qs_array = []
    num_array = []
    for i in qs:
        if (i.value, i.measure_unit.title if i.measure_unit else '') not in qs_array:
            if (str(i.value).split(' ')[0]).isdigit():
                num_array.append((i.value, i.measure_unit.title if i.measure_unit else ''))
            else:
                qs_array.append((i.value,  i.measure_unit.title if i.measure_unit else ''))

    if num_array:
        num_array = set(num_array)
        num_array = sorted(num_array, key=lambda x: int(x[0].title.split(' ')[0]))
    qs_array.extend(num_array)
    # return JsonResponse(f'{num_array}')
    return qs_array


@register.filter
def return_values(values):
    values = filter(lambda v: v != '', values)
    """ this template filter  for return cart item features, gets values   """
    return ProductFeature.objects.filter(id__in=values)


@register.filter
def features(qs, product_id):
    return qs.filter(product_id=product_id).order_by('price')


@register.filter
def filter_feature(qs):
    for val in qs.values('field__is_main'):
        if val['field__is_main']:
            return True
    else:
        return False


@register.simple_tag
def subprice(price, qty):
    return floatformat((float(price) * qty), 0)


@register.filter()
def websitefilter(url):
    if url and url.startswith('http://'):
        return url.split('http://')[1]
    return url.split('https://')[1] if url else ''


@register.simple_tag(name='ignoreusedproducts')
def ignoreused(qs, category_id, used_ids):
    category = Category.objects.get(id=category_id)
    categories = category.get_family().values_list('id', flat=True)
    return qs.filter(category__in=categories).exclude(id__in=used_ids)


def main_category_tree(bred_category, product):
    bin_tree = []
    if bred_category.parent:
        select_main = bred_category
        while select_main.parent:
            bin_tree.append(select_main.parent)
            select_main = select_main.parent
        if select_main not in bin_tree:
            bin_tree.append(select_main)
        bin_tree.reverse()
    else:
        # get all categories of the category tree
        categories_l = bred_category.get_descendants().values_list('id', flat=True)

        filtered_categories = list(filter(lambda x: x.id in categories_l, product.category.all()))

        # warning
        inherit_category = list(filter(lambda x: x.parent in filtered_categories, filtered_categories))

        if inherit_category:
            bin_tree.extend((bred_category, inherit_category[0].parent, inherit_category[0]))
        else:
            if filtered_categories:
                bin_tree.extend([bred_category, filtered_categories[0]])
            else:
                bin_tree.append(bred_category)

    return bin_tree


@register.filter
def breadcrumbs(categories: Category, request):
    slug = request.resolver_match.kwargs.get('slug')

    has_error = False
    try:
        latest_visited_cat = request.META.get('HTTP_REFERER').split('/')[-2]
        bred_category = Category.objects.get(slug=latest_visited_cat, is_active=True)
    except:
        # when user signed in with product link
        has_error = True
        bred_category = categories.first()

    product = Product.objects.get(slug__iexact=slug)

    if has_error:
        get_parent_categories = list(filter(lambda x: x.parent is None, categories.all()))
        if not get_parent_categories:
            bin_tree = main_category_tree(bred_category, product)
        else:
            bred_category = get_parent_categories[0]
            bin_tree = main_category_tree(bred_category, product)
    else:
        bin_tree = main_category_tree(bred_category, product)

    breadcrumb_elements = []
    for item in bin_tree:

        breadcrumb_elements.append(
            (   
                item.get_absolute_url(),
                f"""
                    <a href="{item.get_absolute_url()}" class="linkcolor">
                        <span class="val">{ item.title }</span>
                    </a>
                 """,
                f"""
                <span class="bread-arrow">→</span>
                <li class="breadcrumbs-item">
                    <a href="{item.get_absolute_url()}"
                       class="breadcrumbs-link">{item.title}</a>
                </li>
                """
            )
        )

    return breadcrumb_elements
