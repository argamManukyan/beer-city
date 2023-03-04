import datetime
import json
import time

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.decorators.cache import never_cache

from .email import SendMail
from .forms import UserForm
from .settings import CUSTOM_MESSAGES
from users.models import User, State, Region


class SignupView(View):

    @never_cache
    def get(self, request, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home_page')
        return render(request, 'users/register.html')

    @transaction.atomic
    def post(self, request, **kwargs):
        data = request.POST.dict()
        
        if User.objects.filter(email=data['email']).exists():
            messages.error(request, CUSTOM_MESSAGES['EMAIL_DUPLICATE'])
            return redirect(reverse('users:signup'))

        if data.get('password') != data.get('password2'):
            messages.error(request, CUSTOM_MESSAGES['PASSWORD_MISS_MATCH'])
            return redirect(reverse('users:signup'))
        
        del data['password2']
        del data['submit']
        
        data['username'] = data['email']
        user = User.objects.create_user(**data)
        user.is_active = False
        user.save()
        SendMail.send_activation_message({"user": user, "request": request})
        messages.success(request, CUSTOM_MESSAGES['USER_CREATED'])
        return redirect('users:signin')

class LoginView(View):

    @never_cache
    def get(self, request, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home_page')

        return render(request, 'users/login.html')

    def post(self, request, **kwargs):

        login_value = request.POST.get('email')
        password = request.POST.get('password')
        remember = request.POST.get('remember' or None)

        if not User.objects.filter(email=login_value).distinct().exists():
            messages.error(request, CUSTOM_MESSAGES['USER_WITH_LOGIN_NOT_FOUND'])
            return redirect('users:signin')

        if User.objects.filter(email=login_value, is_active=False).distinct().exists():
            messages.error(request, CUSTOM_MESSAGES['REQUIRED_EMAIL_VERIFICATION'])
            return redirect('users:signin')

        check_user = User.objects.filter(email=login_value).distinct().first()

        user = authenticate(username=check_user.email, password=password)
        if not user:
            messages.error(request, CUSTOM_MESSAGES['INVALID_LOGIN_OR_PASSWORD'])
            return redirect('users:signin')
        else:
            login(request, user)

            if not remember:
                self.request.session.set_expiry(0)
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect('users:profile')


class ActivationEmail(View):

    def get(self, request, **kwargs):

        if request.user.is_authenticated:
            return redirect('home_page')

        try:
            _kw_uid = kwargs.get('uid64')
            _kw_token = kwargs.get('token')
            user_id = force_text(urlsafe_base64_decode(_kw_uid))
            user = User.objects.get(id=user_id)

            if user.is_active:
                return HttpResponse(CUSTOM_MESSAGES['USED_LINK'])

            if PasswordResetTokenGenerator().check_token(user=user, token=_kw_token):
                user.is_active = True
                user.save(force_update=True)
            else:
                user.delete()
                return HttpResponse(CUSTOM_MESSAGES['INVALID_DATA'])

        except User.DoesNotExist:
            return HttpResponse(CUSTOM_MESSAGES['INVALID_DATA'])

        messages.success(request, CUSTOM_MESSAGES['PROFILE_ACTIVATED'])

        data = {}
        data['request'] = request
        data['type'] = 'activation'
        data['email'] = user.email

        return redirect('users:signin')


@login_required
def logout_func(request):
    logout(request)
    return redirect('users:signin')


class ForgotPassword(View):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_page')
        return render(request, 'users/forgot_pass.html')

    def post(self, request):
        username = request.POST.get('login', request.POST.get('email', None))
        if username and username.startswith('+'):
            username = username[1:]

        if not User.objects.filter(email=username).distinct().exists():
            messages.error(request, CUSTOM_MESSAGES['EMAIL_NOT_FOUND'])
            return redirect(reverse('users:password-reset'))

        user = User.objects.filter(email=username).first()
        
        data = {
            "request": request,
            "user": user
        }
        SendMail.send_password_reset_mail(data)

        messages.success(request, CUSTOM_MESSAGES['RESET_SUCCESS'])

        return redirect('users:signin')


class ForgotPasswordConfirm(View):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_page')

        _token = kwargs.get('token')
        _uid = kwargs.get('uid64')

        user_id = urlsafe_base64_decode(_uid).decode()

        try:
            self.user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse(CUSTOM_MESSAGES['USER_NOT_FOUND'])

        if not PasswordResetTokenGenerator().check_token(user=self.user, token=_token):
            messages.error(request, CUSTOM_MESSAGES['INVALID_DATA'])
            return redirect('users:password-reset')

        return render(request, 'users/new_pass_company.html')
    
    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        
        _uid = kwargs.get('uid64')

        user_id = urlsafe_base64_decode(_uid).decode()

        try:
            self.user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse(CUSTOM_MESSAGES['USER_NOT_FOUND'])
        
        if data.get('password') != data.get('password2'):
            messages.error(request, CUSTOM_MESSAGES['PASSWORD_MISS_MATCH'])            
            return redirect(request.build_absolute_uri())
        
        self.user.set_password(data['password'])
        self.user.save()
        messages.success(request, CUSTOM_MESSAGES['SUCCESS_UPDATE_PASSWORD'])
        return redirect('users:signin')        
        

class ProfileView(LoginRequiredMixin, View):
    login_url = 'users:signin'
    redirect_field_name = 'next'

    def get(self, request, **kwargs):
        user: User = request.user
        max_days_count = range(1, 32)

        states = State.objects.all().order_by('id')
        cities = Region.objects.filter(state=states.first())

        if request.is_ajax():

            try:
                cities = Region.objects.filter(Q(state_id=int(request.GET['id'])))
                return JsonResponse(data=list(cities.values('name', 'price', 'id')), safe=False)
            except:
                return JsonResponse(data={}, safe=False)

        # months = list(calendar.month_name)[1:]
        context = {
            "user": user,
            "max_days_count": max_days_count,
            "states": states,
            "cities": cities,
        }
        return render(request, 'users/account.html', context)

    def post(self, request, **kwargs):
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        day = request.POST.get('dd')
        month = request.POST.get('mm')
        year = request.POST.get('yyyy')
        birthday_dtime = None

        if day and day != 'day':
            try:
                birthday_str = f'{day}-{month}-{year}'
                birthday_dtime = datetime.datetime.strptime(birthday_str, '%d-%m-%Y')
            except Exception as e:
                messages.error(request, CUSTOM_MESSAGES['DATETIME_ERROR'])
                return redirect('users:profile')

        
        form = UserForm(request.POST or None, instance=request.user)

        if form.is_valid():
            data = form.save(commit=False)
            if email:
                data.email = email
            if phone_number:
                data.phone_number = phone_number
            if birthday_dtime:
                data.birthday = birthday_dtime
            data.save()
            messages.success(request, CUSTOM_MESSAGES['UPDATE_PERSONAL_DATA_SUCCESS'])
        else:

            error = form.errors.get(list(form.errors.keys())[-1])
            messages.error(request, error)

        return redirect('users:profile')


class PasswordChangeView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request):
        old_password = request.POST.get('oldpassword')
        new_password = request.POST.get('newpassword')

        if not request.user.check_password(old_password):
            messages.error(request, CUSTOM_MESSAGES['WRONG_OLD_PASSWORD'])
            return redirect('users:profile')

        request.user.set_password(new_password)
        user = request.user.save()
        login(request, user)
        messages.success(request, CUSTOM_MESSAGES['SUCCESS_UPDATE_PASSWORD'])

        return redirect('users:profile')


@login_required(login_url='users:signin', redirect_field_name='redirect_to')
def save_user_avatar(request):
    if request.method == 'POST':
        print(request.FILES)
        image = request.FILES.get('avatar')
        fs = FileSystemStorage()
        file = fs.save(image.name, image)

        user: User = request.user
        user.avatar = file
        user.save()

    return redirect('users:profile')
