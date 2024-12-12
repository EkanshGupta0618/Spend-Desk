from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import random
from datetime import datetime
# Create your views here.
# ============================Home Page=========================================
def home_page(request):
    if request.method == 'POST':
        # Get the post data
        uname = request.POST.get('username')
        emaill = request.POST.get('email')
        message = request.POST.get('message')
        # send mail to the admin
        send_mail(
            f'Form submition from {uname}',
            f'Message is: {message}\nEmail: {emaill}',
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        return render(request, 'home.html')
# ===============================================================================
# ============================Login Page=========================================
#For login page of the website
def login_page(request):
    if request.method == 'POST':
        # Get the post data
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user=authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            #return HttpResponse('Invalid Credentials')
            messages.error(request, 'Invalid Username or Password')
    return render(request, 'login.html')
# ===============================================================================
# ============================Signup Page=========================================
#For signup page of the website
def sign_up_page(request):
    if request.method == 'POST':
        # Get the post data
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        # Check if the passwords match   
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        # Check if the username already exists
        elif User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
        # check if the email already exists
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')  
    return render(request, 'signup.html')
# ===============================================================================
# ============================Forgot_Password Page==================================
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            request.session['email'] = email
            send_mail(
                'OTP for password reset',
                f'Your OTP for resetting your password is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return redirect('otp_fill')
        else:
            messages.error(request, 'Email does not exist')
            return redirect('forgot_password')
    return render(request, 'forgot_password.html')
# ==================================================================================
# ============================OTP Fill Page=========================================
def otp_fill(request):
    if request.method == 'POST':
        entered_otp = ''.join(request.POST.getlist('otp'))  # Collect the OTP input values
        session_otp = request.session.get('otp')
        
        if entered_otp == session_otp:
            return redirect('password_reset')  # Redirect to password reset page
        else:
            error = "Invalid OTP. Please try again."
            return render(request, 'otp_fill.html', {'error': error})
    return render(request, 'otp_fill.html')
# =================================================================================
# ============================Password Reset Page=========================================
def password_reset(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            email = request.session.get('email')
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            send_mail(
                'Spend-Desk Password Reset',
                f'Your password has been reset successfully at: {datetime.now()}. If you did not perform this action, please contact us immediately.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return render(request, 'password_reset.html')
    return render(request, 'password_reset.html')
# ===================================================================================
# ============================Dashboard Page=========================================