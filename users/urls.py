from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'users'

urlpatterns = [
    path('signup/', csrf_exempt(SignupView.as_view()), name='signup'),
    path('signup-password/', csrf_exempt(SetPasswordForSignup.as_view()), name='set_password'),
    path('login/', csrf_exempt(LoginView.as_view()), name='signin'),
    path('logout/', csrf_exempt(logout_func), name='logout'),
    path('check-otp/', csrf_exempt(check_otp), name='check_otp'),
    path('activate/<uid64>/<token>/', ActivationEmail.as_view(), name='activate'),
    path('password-reset-confirm/<uid64>/<token>/', csrf_exempt(ForgotPasswordConfirm.as_view()),
         name='password-reset-confirm'),
    path('forgot-password/', ForgotPassword.as_view(), name='password-reset'),
    path('forgot-otp/', ForgotOTP.as_view(), name='forgot-otp'),
    path('me/', csrf_exempt(ProfileView.as_view()), name='profile'),
    path('change-password/', csrf_exempt(PasswordChangeView.as_view()), name='change_password'),
    path('add-photo/', csrf_exempt(save_user_avatar), name='add_photo'),
    path('resend_otp_code/', csrf_exempt(resend_otp_code), name='resend_otp_code'),
    path('delete_user/', csrf_exempt(delete_user), name='delete_user'),
    path('delete_user_photo/', csrf_exempt(delete_user_photo), name='delete_user_photo')
]