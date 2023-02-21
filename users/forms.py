from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .settings import CUSTOM_MESSAGES
from .models import User


class GenericValidatedForm(ModelForm):

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(CUSTOM_MESSAGES['EMAIL_DUPLICATE'])


class UserCompanyModelForm(GenericValidatedForm):
    class Meta:
        model = User
        fields = [
            'company_name',
            'register_city',
            'register_state',
            'register_address',
            'fact_city',
            'fact_state',
            'fact_address',
            'resfirst_name',
            'reslast_name',
            'res_position',
            'tin',
            'phone_number',
            'company_website',
            'company_spher',
        ]


class UserForm(GenericValidatedForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'city',
            'state',
            'address',
        ]

