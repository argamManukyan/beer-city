import json

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from breadcrumbs.models import BreadcrumbTexts
from flatpages.forms import ContactUsForm
from flatpages.models import *
from shop.views import get_ip


def flatpages(request, slug):
    page = get_object_or_404(FlatPages, slug=slug)
    return render(request, 'flatpages/static_pages.html', {'page': page})


def blog_category(request, slug):
    category = get_object_or_404(BlogCategory, slug=slug)
    posts = Blog.objects.filter(category=category)
    categories = BlogCategory.objects.all()

    paginator = Paginator(posts, 12)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        "category": category,
        "categories": categories,
        "page_obj": page_obj
    }
    return render(request, 'flatpages/blog.html', context)


def blog_list(request):
    posts = Blog.objects.all()
    categories = BlogCategory.objects.all()
    st_content = BreadcrumbTexts.objects.filter(location='blog').first()

    paginator = Paginator(posts, 12)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        "categories": categories,
        "page_obj": page_obj,
        "st_content": st_content
    }
    return render(request, 'flatpages/blog_list.html', context)


def blog_details(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    related_posts = Blog.objects.exclude(id=post.id).order_by('?')[:16]

    if post.slug not in request.session:
        request.session[post.slug] = post.slug
        post.views_count += 1
        post.save()

    is_liked = BlogLike.objects.filter(blog_id=post.id, device=get_ip(request)).exists()

    context = {
        "related_posts": related_posts,
        "post": post,
        "is_liked": is_liked,
    }
    return render(request, 'flatpages/blog_details.html', context)


def like_post(request):
    # like or dislike
    data = json.loads(request.body)
    post_id = data['post_id']

    if BlogLike.objects.filter(device=get_ip(request), blog_id=post_id).exists():
        BlogLike.objects.filter(device=get_ip(request), blog_id=post_id).delete()
    else:
        BlogLike.objects.create(device=get_ip(request), blog_id=post_id)

    post = Blog.objects.get(pk=post_id)

    return JsonResponse({"likes_count": post.likes_count})


def gallery_list(request):

    gallery_list = Gallery.objects.all()
    gallery_categories = GalleryCategory.objects.all()
    st_content = BreadcrumbTexts.objects.filter(location='gallery').first()

    paginator = Paginator(gallery_list, 20)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'gallery_categories': gallery_categories,
        'st_content': st_content
    }

    return render(request, 'flatpages/gallery.html', context)


def gallery_details(request, slug):
    gallery_category = get_object_or_404(GalleryCategory, slug=slug)
    images = Gallery.objects.filter(category=gallery_category)
    gallery_categories = GalleryCategory.objects.all()

    paginator = Paginator(images, 20)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        "gallery_category": gallery_category,
        "page_obj": page_obj,
        "gallery_categories": gallery_categories,
    }

    return render(request, 'flatpages/gallery_details.html', context)


def contact_us(request):

    themes = ContactUsThemes.objects.all()
    contact_icons = ContactUsIcons.objects.all()
    st_content = BreadcrumbTexts.objects.filter(location='contacts').first()
    form = ContactUsForm(request.POST)

    if request.method == 'POST':
        theme = None
        if request.POST.get('question') and request.POST.get('question').isdigit():
            theme = ContactUsThemes.objects.filter(id=request.POST.get('question')).first()

        if form.is_valid():
            contact_form = form.save(commit=False)
            if theme:
                contact_form.question = theme
            contact_form.save()

            messages.success(request, _("Ձեր հարցումը հաջողությամբ ուղարկվել է"))
        else:
            messages.error(request, _("Տեղի է ունեցել սխալ։ Խնդրում ենք փորձել կրկին"))

        return redirect('contacts')

    context = {
        "themes": themes,
        "contact_icons": contact_icons,
        'st_content': st_content
    }

    return render(request, 'flatpages/contacts.html', context)


def faq_view(request):
    questions = FAQModel.objects.all()
    return render(request, 'flatpages/faq.html', {'questions': questions})