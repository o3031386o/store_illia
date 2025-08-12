from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required



@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید.')
    return redirect('login')

# views.py

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


# views.py
from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect
from django.contrib import messages

User = get_user_model()


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'رمز عبور و تکرار آن یکسان نیستند.')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'این نام کاربری قبلاً استفاده شده است.')
            return redirect('signup')

        # ساخت کاربر جدید
        user = User.objects.create_user(username=username, password=password1)
        messages.success(request, 'ثبت‌نام با موفقیت انجام شد.')

        # ورود خودکار بعد از ثبت‌نام
        login(request, user)
        return redirect('home')  # به صفحه اصلی یا هر صفحه دیگر

    return render(request, 'signup.html')

