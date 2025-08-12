from django.shortcuts import render

# Create your views here.

# views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'با موفقیت وارد شدید.')
            return redirect('home')  # به صفحه اصلی یا هر صفحه‌ای که خواستی
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید.')
    return redirect('login')

# views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.user.is_authenticated:
        redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید.')
                return redirect('home')  # به صفحه اصلی یا هر صفحه‌ای که خواستی
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
        return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید.')
    return redirect('login')

