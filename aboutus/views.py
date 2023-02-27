from django.shortcuts import render
from breadcrumbs.models import BreadcrumbTexts
from flatpages.models import Blog
from shop.models import Bullets
from .models import *


def about_us(request):
    abouts: AboutUs = AboutUs.objects.first()
    our_goals = OurGoals.objects.all()
    goal_img = GoalImage.objects.first()
    posts = Blog.objects.all()[:3]
    bullets = Bullets.objects.all()
    st_content = BreadcrumbTexts.objects.filter(location='abouts').first()
    file_extension = 'video' if abouts and abouts.file and abouts.file.name.split('.')[:1] in ['flv', 'mp4'] else 'photo'
    partners = Partners.objects.all()
    
    context = {
        "abouts": abouts,
        "our_goals": our_goals,
        "partners": partners,
        "goal_img": goal_img,
        "bullets": bullets,
        "posts": posts,
        "st_content": st_content,
        "file_extension": file_extension,
    }

    return render(request, 'flatpages/about_us.html', context)