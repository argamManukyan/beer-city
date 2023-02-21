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
from .forms import UserCompanyModelForm, UserForm
from .settings import CUSTOM_MESSAGES
from users.models import User, State, Country


def check_otp(request):

    if request.is_ajax() and 'phone_number' not in request.session:
        data = json.loads(request.body)
        verify_code = data['verify_code']
        phone_number = data['phone_number'][1:]
    else:
        data = json.loads(request.body)
        verify_code = data['verify_code']
        phone_number = request.session['phone_number']
    print(phone_number)
    print(verify_code)
    user = User.objects.filter(phone_number=phone_number).first()
    print(user)
    if not user:
        messages.error(request, CUSTOM_MESSAGES['USER_NOT_FOUND'])
        return JsonResponse({"not_found": CUSTOM_MESSAGES['USER_NOT_FOUND']}, status=400)

    if verify_code != user.verification_code:
        print(user.verification_code, "USER CODE")
        if user.attempts_count >= 1:
            user.attempts_count -= 1
            user.save()
            return JsonResponse({"otp_error": CUSTOM_MESSAGES['OTP_ERROR']}, status=400)
        messages.error(request, CUSTOM_MESSAGES['SMTH_WENT_WRONG'])
        user.delete()
        return JsonResponse({"otp_link": request.build_absolute_uri(reverse('users:signup'))}, status=400)
    else:
        user.verification_code = None
        user.sent_verification_code = False
        user.phone_verified = True
        user.email_verified = True
        user.is_active = True
        user.attempts_count = 4
        request.session['phone_number'] = phone_number
        user.save()

        return JsonResponse({"otp_right": CUSTOM_MESSAGES['OTP_RIGHT']})


def resend_otp_code(request):
    data = json.loads(request.body)
    phone_number = data.get('phone_number')[1:] if data.get('phone_number') and len(data['phone_number']) > 1 else request.session.get('phone_number')
    phone_number = str(phone_number).replace(' ', '')

    if not User.objects.filter(phone_number=phone_number).exists():
        return JsonResponse({"url": request.build_absolute_uri(reverse('users:signup'))}, status=400)

    user = User.objects.get(phone_number=phone_number)
    if user.attempts_count == 0:
        user.delete()
        return JsonResponse({"url": request.build_absolute_uri(reverse('users:signin'))}, status=400)

    message_text = 'Verification code: '
    if request.LANGUAGE_CODE == 'hy':
        message_text = 'Հաստատման կոդ: '
    elif request.LANGUAGE_CODE == 'ru':
        message_text = 'Код верификации: '
    user.send_otp_code(message_text)

    return HttpResponse(status=200)


def delete_user(request):
    data = json.loads(request.body)
    phone_number = data['phone_number'].replace(' ', '')
    phone_number = phone_number[1:]
    User.objects.filter(phone_number=phone_number).delete()
    return JsonResponse({'url': request.build_absolute_uri(reverse('users:signup'))})


@login_required(login_url='users:signup', redirect_field_name='redirect_to')
def delete_user_photo(request):
    user: User = request.user
    user.avatar.delete()
    return redirect('users:profile')


class SignupView(View):

    @never_cache
    def get(self, request, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home_page')
        return render(request, 'users/register.html')

    @transaction.atomic
    def post(self, request, **kwargs):

        if request.is_ajax():
            json_data = json.loads(request.body)
            if 'email' in json_data and json_data.get('account_type') == 'personal':
                username = f"{json_data['email'].split('@')[0]}-{str(int(time.time()))}"
                data = {k: v for k, v in json_data.items() if k not in ['submit', 'csrfmiddlewaretoken', 'phone']}

                data['phone_number'] = f'{data["phone_number"]}{json_data["phone"].replace(" ", "")}'

                if User.objects.filter(phone_number=data['phone_number']).exists():
                    messages.error(request, CUSTOM_MESSAGES['PHONE_NUMBER_DUPLICATE'])
                    return JsonResponse({"url": request.build_absolute_uri()}, status=400)

                if User.objects.filter(email=data['email']).exists():
                    messages.error(request, CUSTOM_MESSAGES['EMAIL_DUPLICATE'])
                    return JsonResponse({"url": request.build_absolute_uri()}, status=400)

                if User.objects.filter(blocked_time__isnull=False, phone_number=data['phone_number']).exists():
                    messages.error(request, CUSTOM_MESSAGES['BLOCKED_TIME'])
                    return JsonResponse({"url": request.build_absolute_uri()}, status=400)

                user = User.objects.create_user(username, **data)
                user.is_active = False
                user.save()

                if data['account_type'] == 'personal':

                    message_text = 'Verification code: '
                    if request.LANGUAGE_CODE == 'hy':
                        message_text = 'Հաստատման կոդ: '
                    elif request.LANGUAGE_CODE == 'ru':
                        message_text = 'Код верификации: '
                    user.send_otp_code(message_text)

                    return JsonResponse({"sent_code": True})
        else:
            json_data = request.POST

            data = {'phone_number': json_data['companyPhone'][1:] if json_data['companyPhone']\
                .startswith('+') else f"{json_data['companyPhone']}",
                    'password': json_data['companyPassword'],
                    'email': json_data['email'],
                    'company_name': json_data['companyName'],
                    "account_type": 'company',
                    "username": json_data['email'].split('@')[0] + f'{int(time.time())}'
                    }

            if User.objects.filter(phone_number=data['phone_number']).exists():
                messages.error(request, CUSTOM_MESSAGES['PHONE_NUMBER_DUPLICATE'])
                return redirect(reverse('users:signup') + '?company=True')

            if User.objects.filter(email=data['email']).exists():
                messages.error(request, CUSTOM_MESSAGES['EMAIL_DUPLICATE'])
                return redirect(reverse('users:signup') + '?company=True')

            user = User.objects.create_user(**data)
            user.is_active = False
            user.save()
            SendMail.send_activation_message({"user": user, "request": request})
            messages.success(request, CUSTOM_MESSAGES['USER_CREATED'])
            return redirect('users:signin')


class SetPasswordForSignup(View):

    def get(self, request, **kwargs):
        if 'phone_number' not in self.request.session:
            return redirect('users:signup')
        return render(request, 'includes/register-password.html')

    def post(self, request, **kwargs):
        password = request.POST.get('companyPassword')
        user = get_object_or_404(User, phone_number=request.session['phone_number'])
        user.set_password(password)
        user.save()
        authenticate(request, username=user.email, password=password)
        login(request, user)
        if 'phone_number' in request.session:
            del request.session['phone_number']
        return redirect('users:profile')


class LoginView(View):

    @never_cache
    def get(self, request, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home_page')

        return render(request, 'users/login.html')

    def post(self, request, **kwargs):

        login_value = request.POST.get('login')
        if login_value and login_value.startswith('+'):
            login_value = login_value.replace(' ', '')[1:]
        elif login_value and login_value.isdigit():
            login_value = login_value.replace(' ', '')

        password = request.POST.get('password')
        remember = request.POST.get('remember' or None)

        if not User.objects.filter(Q(email=login_value) | Q(phone_number=login_value)).distinct().exists():
            messages.error(request, CUSTOM_MESSAGES['USER_WITH_LOGIN_NOT_FOUND'])
            return redirect('users:signin')

        if User.objects.filter(Q(email=login_value) | Q(phone_number=login_value),
                               Q(phone_verified=False, email_verified=True)).distinct().exists():
            messages.error(request, CUSTOM_MESSAGES['REQUIRED_PHONE_VERIFICATION'])
            return redirect('users:signin')

        if User.objects.filter(Q(email=login_value) | Q(phone_number=login_value),
                               Q(phone_verified=True, email_verified=False)).distinct().exists():
            messages.error(request, CUSTOM_MESSAGES['REQUIRED_EMAIL_VERIFICATION'])
            return redirect('users:signin')

        check_user = User.objects.filter(Q(email=login_value) | Q(phone_number=login_value)).distinct().first()

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
                user.phone_verified = True
                user.email_verified = True
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
        print(request.session.get('phone_number'))
        return render(request, 'users/forgot_pass.html')

    def post(self, request):
        username = request.POST.get('login', request.POST.get('email', None))
        if username and username.startswith('+'):
            username = username[1:]

        if not User.objects.filter(Q(email=username) | Q(phone_number=username),
                               account_type=request.POST.get("account_type")).distinct().exists():
            messages.error(request, CUSTOM_MESSAGES['EMAIL_NOT_FOUND'])
            return redirect(reverse('users:password-reset') + f'?account_type={request.POST.get("account_type")}')

        if '@' in username and User.objects.filter(email=username, email_verified=False).exists():
            messages.error(request, CUSTOM_MESSAGES['VERIFY_EMAIL'])
            return redirect(reverse('users:password-reset') + f'?account_type={request.POST.get("account_type")}')

        if not User.objects.filter(Q(email=username) | Q(phone_number=username),
                                   email_verified=True, phone_verified=True,
                                   account_type=request.POST.get("account_type")).distinct().exists():
            messages.error(request, CUSTOM_MESSAGES['SMTH_WENT_WRONG'])
            return redirect(reverse('users:password-reset') + f'?account_type={request.POST.get("account_type")}')

        if username.find('@') == -1 :
            request.session['phone_number'] = username
            print(username, "USER PASSWORD")
            user = User.objects.filter(phone_number=username).first()
            message_text = 'Verification code: '
            if request.LANGUAGE_CODE == 'hy':
                message_text = 'Հաստատման կոդ: '
            elif request.LANGUAGE_CODE == 'ru':
                message_text = 'Код верификации: '
            user.send_otp_code(message_text)


            return redirect(reverse('users:forgot-otp') + f'?account_type={request.POST.get("account_type")}')

        data = {}
        data['request'] = request
        data['user'] = User.objects.filter(Q(email=username) | Q(phone_number=username)).distinct().first()
        SendMail.send_password_reset_mail(data)

        messages.success(request, CUSTOM_MESSAGES['RESET_SUCCESS'])

        return redirect('users:signin')


class ForgotOTP(View):

    def get(self, request, **kwargs):
        if self.request.user.is_authenticated or 'phone_number' not in request.session:
            return redirect('home_page')
        return render(request, 'users/forgot-otp.html')

    def post(self, request, **kwargs):

        data = json.loads(request.body)

        user = User.objects.filter(phone_number=data['phone_number']).first()
        print(data, 'BODY')
        if user.verification_code != data['verify_code']:
            return HttpResponse(status=400)

        user.verification_code = ''
        user.save()

        return HttpResponse(status=200)


class ForgotPasswordConfirm(View):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_page')

        if 'phone_number' not in request.session:
            _token = kwargs.get('token')
            _uid = kwargs.get('uid64')

            session_token = request.session.get('password_reset_token')
            user_id = urlsafe_base64_decode(_uid).decode()

            try:
                self.user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return HttpResponse(CUSTOM_MESSAGES['USER_NOT_FOUND'])

            if not PasswordResetTokenGenerator().check_token(user=self.user, token=_token) \
                    or not session_token:
                messages.error(request, CUSTOM_MESSAGES['INVALID_DATA'])
                return redirect('users:password-reset')

        return render(request, 'users/new_pass_company.html')

    def post(self, request, **kwargs):

        if 'phone_number' not in request.session:
            form = request.POST.get('companyPassword')
            _uid = kwargs.get('uid64')
            user_id = urlsafe_base64_decode(_uid).decode()

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return HttpResponse(CUSTOM_MESSAGES['USER_NOT_FOUND'])

            user.set_password(form)
            user.save()
            messages.success(request, CUSTOM_MESSAGES['PASSWORD_UPDATE_SUCCESS'])
            return redirect('users:signin')
        else:
            try:
                user = User.objects.get(phone_number=request.session['phone_number'])
            except:
                raise Http404

            form = request.POST.get('companyPassword')
            user.set_password(form)
            user.save()
            messages.success(request, CUSTOM_MESSAGES['PASSWORD_UPDATE_SUCCESS'])
            return redirect('users:signin')


class ProfileView(LoginRequiredMixin, View):
    login_url = 'users:signin'
    redirect_field_name = 'next'

    def get(self, request, **kwargs):
        user: User = request.user
        max_days_count = range(1, 32)

        states = State.objects.all().order_by('id')
        cities = Country.objects.filter(state=states.first())

        if request.is_ajax():

            try:
                cities = Country.objects.filter(Q(state_id=int(request.GET['id'])))
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

        if email:
            if request.user.email != email:
                if User.objects.filter(email=email).exists():
                    messages.error(request, CUSTOM_MESSAGES['EMAIL_DUPLICATE'])
                    return redirect('users:profile')
            else:
                email = None

        if phone_number:
            if request.user.phone_number != phone_number:
                if User.objects.filter(phone_number=phone_number).exists():
                    messages.error(request, CUSTOM_MESSAGES['EMAIL_DUPLICATE'])
                    return redirect('users:profile')
            else:
                phone_number = None

        form = UserCompanyModelForm(request.POST, instance=request.user) \
            if request.user.account_type == 'company' \
            else UserForm(request.POST or None, instance=request.user)

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
