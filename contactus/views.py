from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from breadcrumbs.models import BreadcrumbTexts
from .email import SendMailThread
from .forms import ContactUsForm
from .models import ContactUsPage


def contact_us(request):
    form = ContactUsForm(request.POST or None)
    st_content: BreadcrumbTexts = BreadcrumbTexts.objects.filter(location='contacts').first()
    contactuspage: ContactUsPage = ContactUsPage.objects.first()

    if request.method == 'POST':
        if form.is_valid():
            form = form.save()
            
            messages.add_message(request, messages.SUCCESS,
                                 _('Ձեր Հաղորդագրությունը հաջողությամբ ուղարկված է:<br>Մեր մենեջերը '
                                   'շուտով կապ կհաստատի Ձեզ հետ:'))
            data = {
                'action': 'contact',
                'request': request,
                'name': form.name,
                'email': form.email,
                'message': form.message,
            }
            
            message = f""" Դուք ստացել եք հետադարձ կապի նամակ \n
                           Անուն և ազգանուն: {data['name']} \n
                           Էլ. հասցե: {data['email']} \n
                           Նամակ: {data["message"]} \n
                      """
            
            send_mail("Հետադարձ կապի պատվեր", message=message, from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[settings.EMAIL_HOST_USER], html_message=message, fail_silently=True)
        else:
            messages.add_message(request, messages.ERROR, _('Տեղի էունեցել սխալ'))
        return redirect('contact_us')

    context = {
        'st_content': st_content,
        'contactuspage': contactuspage, 
        'contact_icons': contactuspage.contact_icons.all() if contactuspage else [],
        'contact_icons': contactuspage.social_buttons.all()  if contactuspage else [],
        }
    
    return render(request, 'flatpages/contacts.html', context)
