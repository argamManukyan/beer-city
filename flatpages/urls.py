from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from aboutus.views import about_us
from .views import *


urlpatterns = [
    path('blog/', blog_list, name='blog_list'),
    path('blog/<slug>/', blog_details, name='blog_details'),
    path('blog-category/<slug>/', blog_category, name='blog_category'),
    path('gallery/', gallery_list, name='gallery_list'),
    path('gallery/<slug>/', gallery_details, name='gallery_details'),
    path('contacts/', csrf_exempt(contact_us), name='contacts'),
    path('faq/', faq_view, name='faq'),
    path('about-us/', about_us, name='about_us'),
    path('<slug>/', flatpages, name='flatpages'),
]