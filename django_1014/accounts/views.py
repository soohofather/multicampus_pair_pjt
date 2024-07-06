from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import User
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):

    user = User.objects.all()

    context = {
        "user": user,
    }
    return render(request, "accounts/index.html", context)


def signup(request):

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 회원가입하면 로그인 유지 되도록 하는 코드
            auth_login(request, user)
            return redirect("reviews:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }

    return render(request, "accounts/signup.html", context=context)


def login(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            else:
                return redirect("reviews:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }

    return render(request, "accounts/login.html", context)


def logout(request):
    auth_logout(request)
    return redirect("reviews:index")


def detail(request, pk):
    user = User.objects.get(pk=pk)

    context = {
        "user": user,
    }
    return render(request, "accounts/detail.html", context)


def delete(request, pk):

    user = User.objects.get(pk=pk)

    user.delete()

    return redirect("accounts:index")


@login_required
def update(request, pk):

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:detail", request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)
