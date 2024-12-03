from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
# Create your views here.

def index_page(request):
    return render(request, 'index.html')



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


def forgot_password(request): 
    if request.method == 'POST':
        # Get the post data
        email = request.POST.get('email')
        print ("Email: ", email)
        if User.objects.filter(email=email).exists():
            print('Email exists')
            
        return render(request, 'forgot_password.html')
    return render(request, 'forgot_password.html')


def otp_fill(request):
    return render (request, 'otp_fill.html')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')