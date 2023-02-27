from django.forms import ModelForm


from .models import ContactUs


class ContactUsForm(ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'message', 'phone_number']