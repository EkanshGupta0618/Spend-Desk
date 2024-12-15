from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import plotly.graph_objects as go
import plotly.colors
from .models import Budget, Expense
from django.db.models import Sum
import random
from django.db.models.functions import ExtractMonth
from datetime import datetime
import calendar
# ===============================================================================
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
# ============================Password Reset Page==================================
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

@login_required(login_url='login')
def dashboard(request):
    # Fetch the user's budget
    budget = Budget.objects.filter(user=request.user).first()
    current_budget = budget.monthly_budget if budget else 0.0

    # Fetch expenses
    expenses = Expense.objects.filter(user=request.user)

    # Calculate remaining budget
    total_expenses = sum(exp.amount for exp in expenses)
    remaining_budget = current_budget - total_expenses

    # Aggregate expenses by category
    expense_data = expenses.values('category').annotate(total_amount=Sum('amount'))

    # Prepare data for the pie chart
    categories = [data['category'] for data in expense_data]
    amounts = [data['total_amount'] for data in expense_data]
    pull = [0.1] * (len(categories) - 1)  # Pull out the first slice

    
    # Check if there are any expenses to display
    if not categories or not amounts:
        categories = ['No Expenses']
        amounts = [1]  # To show a single slice in the pie chart
        show_chart = False  # Flag to indicate that the chart should not be shown
    else:
        show_chart = True  # Flag to indicate that the chart should be shown

    # Create a Plotly pie chart with enhanced styling
    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=amounts,
        hole=0.3,  # For a donut chart
        textinfo='label+percent',  # Show label and percentage
        hoverinfo='label+percent+value',  # Show label, percentage, and value on hover
        hovertemplate='<b>%{label}</b><br>Amount: Rs.%{value}<br>Percentage: %{percent:.2%}<extra></extra>',  # Custom hover template
        textfont=dict(
            family="Arial, sans-serif",
            size=14,
            color='white'
        ),
        marker=dict(
            colors=plotly.colors.qualitative.Plotly,  # Use Plotly's qualitative colors
            line=dict(color='#FFFFFF', width=2)  # White border for slices
        ),
        pull=pull  # Pull out the first slice
    )])
    
    fig.update_traces(marker=dict(line=dict(width=2, color='white')), selector=dict(type='pie'))  
    # Update layout for better aesthetics
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Arial, sans-serif"
        )
    )

    # # Update layout for better aesthetics
    fig.update_layout(
        annotations=[dict(text='Expenses', x=0.5, y=0.5, font_size=20, showarrow=False)],
        showlegend=True,
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=0, r=0, t=50, b=0),  # Remove margins
        height=500,  # Set height for the chart
        template='plotly_white'  # Use a clean white template
    )

    # Generate HTML for the chart
    chart_html = fig.to_html(full_html=False) if show_chart else None

    return render(request, 'dashboard.html', {
        'budget': current_budget,
        'remaining': remaining_budget,
        'expenses': expenses,
        'chart_html': chart_html,  # Pass the chart HTML to the template
        'show_chart': show_chart,  # Pass the flag to the template
        'messages': messages.get_messages(request)
    })

# ==================================================================================
# ============================= Budget Page=========================================
@login_required(login_url='login')
def set_budget(request):
    if request.method == 'POST':
        budget_amount = request.POST.get('monthly_budget')
        
        # Get or create the user's budget
        budget, created = Budget.objects.get_or_create(user=request.user)
        
        # Update the monthly budget
        budget.monthly_budget = budget_amount
        budget.save()
        
        messages.success(request, 'Monthly budget set successfully!')
        return redirect('dashboard')  # Redirect to the dashboard after setting the budget

    return redirect('dashboard')  # Redirect if not a POST request
# ==================================================================================
# ============================= Add Expense Page====================================
@login_required(login_url='login')
def add_expense(request):
    if request.method == 'POST':
        expense_id = request.POST.get('expense_id')
        if expense_id:  # If expense_id is present, update the expense
            expense = get_object_or_404(Expense, id=expense_id, user=request.user)
            expense.description = request.POST.get('description')
            expense.amount = request.POST.get('amount')
            expense.category = request.POST.get('category')
            expense.save()
            messages.success(request, 'Expense updated successfully!')
        else:  # Otherwise, create a new expense
            description = request.POST.get('description')
            amount = request.POST.get('amount')
            category = request.POST.get('category')
            Expense.objects.create(
                user=request.user,
                description=description,
                amount=amount,
                category=category
            )
            messages.success(request, 'Expense added successfully!')
        return redirect('dashboard')  # Redirect to the dashboard after adding/updating the expense
    return redirect('dashboard')  # Redirect if not a POST request
# ==================================================================================
# ============================= Edit Expense Page===================================
@login_required(login_url='login')
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.description = request.POST.get('description')
        expense.amount = request.POST.get('amount')
        expense.category = request.POST.get('category')
        expense.save()
        messages.success(request, 'Expense updated successfully!')
        return redirect('dashboard')
    return redirect('dashboard')  # Redirect if not a POST request
# ==================================================================================
# ============================= Delete Expense Page=================================
@login_required(login_url='login')
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('dashboard')
    return redirect('dashboard')  # Redirect if not a POST request
# ==================================================================================