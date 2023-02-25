from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'users'

urlpatterns = [
    path('signup/', csrf_exempt(SignupView.as_view()), name='signup'),
    path('login/', csrf_exempt(LoginView.as_view()), name='signin'),
    path('logout/', csrf_exempt(logout_func), name='logout'),
    path('activate/<uid64>/<token>/', ActivationEmail.as_view(), name='activate'),
    path('password-reset-confirm/<uid64>/<token>/', csrf_exempt(ForgotPasswordConfirm.as_view()),
         name='password-reset-confirm'),
    path('forgot-password/', ForgotPassword.as_view(), name='password-reset'),
    path('me/', csrf_exempt(ProfileView.as_view()), name='profile'),
    path('change-password/', csrf_exempt(PasswordChangeView.as_view()), name='change_password'),
]