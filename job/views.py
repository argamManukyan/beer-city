from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from breadcrumbs.models import BreadcrumbTexts
from videos.models import Video
from .forms import SubmitFileForm, CustomCVForm
from .models import JobItem, JobCategory, CustomResumeForJob, PhoneNumbers

ADMIN_EMAIL = settings.EMAIL_HOST_USER


def job_list(request):
    jobs = JobItem.objects.filter(is_active=True).order_by('-id')
    video = Video.objects.filter(location='job').first()
    st_content = BreadcrumbTexts.objects.filter(location='job').first()
    job_categories = JobCategory.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(jobs, 12)
    page_obj = paginator.get_page(page)

    return render(request, 'job/job.html',
                  context={
                      'page_obj': page_obj,
                      'st_content': st_content,
                      'job_categories': job_categories,
                      'video': video
                  }
                  )


def job_category(request, slug):
    category = get_object_or_404(JobCategory, slug=slug)
    job_categories = JobCategory.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(category.jobitem_set.filter(is_active=True).order_by('-id'), 12)
    page_obj = paginator.get_page(page)
    video = Video.objects.filter(location='job').first()

    return render(request, 'job/job_category.html',
                  context={
                      'page_obj': page_obj,
                      'category': category,
                      'job_categories': job_categories,
                      'video': video
                  }
                  )


def job_details(request, slug):
    job = get_object_or_404(JobItem, slug=slug)
    form = SubmitFileForm(request.POST, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            resume = form.save()
            message = render_to_string("job/email/submit_cv.html", context={"job": resume.job}, request=request)
            msg = EmailMessage(resume.job.name, body=message, from_email=ADMIN_EMAIL, to=[ADMIN_EMAIL])
            msg.content_subtype = "html"
            msg.attach_file(resume.cv.path)
            msg.send()

            messages.success(request, _("Ձեր CV -ն հաջողությամբ ուղարկվել է:"))
        else:
            messages.error(request, _("Տեղի է ունեցել սխալ, խնդրում ենք փորձել կրկին:"))
        return redirect('jobs:job_details', slug=slug)

    return render(request, 'job/job_full.html', context={'job': job})


def create_sv(request, slug):
    job = get_object_or_404(JobItem, slug=slug)
    context = {'job': job}

    form = CustomCVForm(request.POST, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            cv = form.save()
            cv = CustomResumeForJob.objects.get(pk=cv.id)
            cv.job = job
            cv.gender = request.POST['gender']
            phone_numbers = request.POST.getlist('phone', None)
            if phone_numbers:
                for phone_number in phone_numbers:
                    pn, created = PhoneNumbers.objects.get_or_create(phone=phone_number)
                    cv.phone.add(pn.id)
            cv.save()

            html_message = render_to_string('job/email/create_cv_pdf.html',
                                            context={"cv": cv, "job": job}, request=request)
            return html_to_pdf(html_message)

            # messages.success(request, _("Ձեր CV -ն հաջողությամբ ուղարկվել է:"))
        else:
            print(form.errors)
            messages.error(request, _("Տեղի է ունեցել սխալ, խնդրում ենք փորձել կրկին:"))
        return redirect('jobs:job_details', slug=slug)

    return render(request, 'job/create_cv.html', context)


# defining the function to convert an HTML file to a PDF file
def html_to_pdf(html):
    import pdfkit
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type='application/pdf')
    return response
