from django.shortcuts import render, redirect, get_object_or_404

# 회원가입 form import
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model

# login, logout 내장 form import
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# 회원인증
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# 메시지알림
from django.contrib import messages

# 로그인되어야지만 들어가지게 설정
from django.contrib.auth.decorators import login_required

# 비밀번호 변경
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.


@login_required
def index(request):
    user = get_user_model().objects.all()
    context = {"user": user}
    return render(request, "accounts/index.html", context)


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # ModelForm의 save 메서드의 리턴값은 해당 모델의 인스턴스다!
            auth_login(request, user)  # 로그인
            messages.success(request, "회원가입이 되었습니다.")
            return redirect("accounts:login")

    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "accounts/signup.html", context)


def detail(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    context = {"user": user}
    return render(request, "accounts/detail.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get("next") or "reviews:index")
    else:
        form = AuthenticationForm
    context = {"form": form}
    return render(request, "accounts/login.html", context)


def logout(request):
    auth_logout(request)
    messages.warning(request, "로그아웃 하였습니다.")
    return redirect("reviews:index")


@login_required
def update(request):
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


def withdraw(request, pk):
    get_user_model().objects.get(id=pk).delete()
    return redirect("accounts:index")


def follow(request, pk):
    # 프로필에 해당하는 유저를 로그인한 유저가!
    user = get_object_or_404(get_user_model(), pk=pk)
    if request.user == user:
        messages.warning(request, "스스로 팔로우 할 수 없습니다.")
        return redirect("accounts:detail", pk)
    if request.user in user.followers.all():
        # (이미) 팔로우 상태이면, '팔로우 취소'버튼을 누르면 삭제 (remove)
        user.followers.remove(request.user)
    else:
        # 팔로우 상태가 아니면, '팔로우'를 누르면 추가 (add)
        user.followers.add(request.user)
    return redirect("accounts:detail", pk)


@login_required
def password_edit(request):
    if request.method == "POST":

        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password successfully changed")
            return redirect("accounts:login")
        else:
            messages.error(request, "Password not changed")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "accounts/password.html", {"form": form})
