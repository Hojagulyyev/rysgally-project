from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib import messages
from django.urls import reverse


# ========== VIEWS ==========

def signup_view(request):
    return render(request, "users/signup.html")


def login_view(request):
    context = {
        "users": User.objects.all()
    }
    return render(request, "users/login.html", context)


# ========== INTERACTORS ==========

def signup(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    User.objects.create_user(
        username=username,
        password=password,
    )
    return redirect('users:login_view')


def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = authenticate(username=username, password=password)

    if user is None:
        messages.error(request, "These credentials are incorrect")
        return redirect(
            f"{reverse('users:login_view')}"
            f"?username={username}"
        )

    login(request, user)
    return redirect('commits:commits_view')


@login_required
def logout(request):
    logout(request)
    return redirect('users:login_view')
