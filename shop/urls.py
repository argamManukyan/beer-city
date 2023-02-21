from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('subscribe/', CreateSubscriptionView.as_view(), name='subscribe'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('catalog/<slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('products/<slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('offer/', SaleOfferNewBestSellerView.as_view(), name='offers'),
    path('search/', SearchView.as_view(), name='search'),
]
