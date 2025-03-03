from django.shortcuts import render, redirect
from accounts.forms import SignUpForm, LogInForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from functools import wraps
from django.contrib.auth.models import User

# Create your views here.
''' <------------------------- Check Login User ---------------------------> '''
def login_excluded(redirect_to):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            return view(request, *args, **kwargs)
        return wrapper
    return decorator
''' <------------------------ End Check Login User ------------------------> '''


''' <---------------------------- User Sign Up ----------------------------> '''
@login_excluded('dashboards:dashboard')
def signup_view(request):
    next = request.GET.get('next')
    form = SignUpForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username    = form.cleaned_data.get('username')
            password    = form.cleaned_data.get('password1')
            user        = authenticate(username = username, password = password)
            login(request, user)
            if next:
                messages.success(request, f'You are now logged in as {username}.')
                return redirect(next)
            messages.success(request, f'You are now logged in as {username}.')
            return redirect('dashboards:dashboard')

    context = {
        'form' : form
    }

    return render(request, 'accounts/signup.html', context)
''' <-------------------------- End User Sign Up --------------------------> '''


''' <----------------------------- User Login -----------------------------> '''
@login_excluded('dashboards:dashboard')
def login_view(request):
    next = request.GET.get('next')
    form = LogInForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username    = form.cleaned_data.get('username')
            password    = form.cleaned_data.get('password')
            user        = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                if next:
                    messages.success(request, f'You are now logged in as {username}.')
                    return redirect(next)
                # Check Group Permission
                group = request.user.groups.values_list('name', flat = True).first()
                if group == 'attache staff':
                    messages.success(request, f'You are now logged in as {username}.')
                    return redirect('c-panels:list-transaction')
                messages.success(request, f'You are now logged in as {username}.')
                return redirect('dashboards:dashboard')
            else:
                messages.error(request, 'Invalid Username or Password')
        else:
            messages.error(request, 'Invalid Username or Password')

    context = {
        'form' : form
    }

    return render(request, 'accounts/login.html', context)
''' <--------------------------- End User Login ---------------------------> '''


''' <----------------------------- User Logout ----------------------------> '''
def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('portalpages:home')
''' <-------------------------- End User Logout ---------------------------> '''
