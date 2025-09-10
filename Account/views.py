from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "با موفقیت وارد شدید 🎉")
            return redirect("home")   # بعد از لاگین به صفحه اصلی برو
        else:
            messages.error(request, "نام کاربری یا رمز عبور اشتباه است ❌")

    return render(request, "login.html")



def signup_view(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")

        # اعتبارسنجی ساده
        if not fullname or not email or not username or not password or not confirm_password:
            messages.error(request, "لطفاً همه فیلدها را پر کنید ❌")
            return render(request, "signup.html")

        if password != confirm_password:
            messages.error(request, "رمز عبور و تکرار آن یکسان نیست ❌")
            return render(request, "signup.html")

        # ساخت یوزر
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.first_name = fullname   # می‌تونی full_name رو اینجا ذخیره کنی
            user.save()

            login(request, user)  # بعد از ثبت‌نام، خودکار لاگین میشه
            messages.success(request, "ثبت‌نام موفقیت‌آمیز بود 🎉")
            return redirect("home")

        except Exception as e:
            messages.error(request, f"خطا در ثبت‌نام: {e}")
            return render(request, "signup.html")

    return render(request, "signup.html")
