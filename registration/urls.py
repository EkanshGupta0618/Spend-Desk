"""
URL configuration for registration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views
from app1.views import set_budget, add_expense, get_expenses




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.sign_up_page, name='signup'),                                # SignUpPage to sign_up_page
    path('login/', views.login_page, name='login'),                             # LoginPage to login_page
    path('home/', views.home_page, name='home'),                                # HomePage to home_page
    path('forgot_password/', views.forgot_password, name='forgot_password'),    # ForgotPassword to forgot_password
    path('otp_fill/', views.otp_fill, name='otp_fill'),                         # OTP_Fill to otp_fill
    path('dashboard/', views.dashboard, name='dashboard'),                      # Dashboard to dashboard
    path('password_reset/', views.password_reset, name='password_reset'),       # PasswordReset
    path('set-budget/', set_budget, name='set_budget'),
    path('add-expense/', add_expense, name='add_expense'),
    path('get-expenses/', get_expenses, name='get_expenses'), 
]

