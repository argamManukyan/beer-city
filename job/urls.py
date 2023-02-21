from django.urls import path
from .views import *

app_name = 'jobs'

urlpatterns = [
    path('careers/', job_list, name='job_list'),
    path('careers/<slug>/', job_category, name='job_category'),
    path('career/<slug>/', job_details, name='job_details'),
    path('career/<slug>/create-cv/', create_sv, name='create_cv')
]
