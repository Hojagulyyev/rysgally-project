from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout,
)
from django.contrib import messages
from django.urls import reverse

from apps.commits.services import get_commit_statistic_by_user


# ========== VIEWS ==========

def signup_view(request):
    return render(request, "users/signup.html")


def login_view(request):
    context = {
        "users": User.objects.all()
    }
    return render(request, "users/login.html", context)


@login_required
def detail_view(request, id):
    (
        user_commits,
        user_total_commits,
        user_closed_commits,
        user_undone_commits,
        user_commit_progress_in_percentage
    ) = get_commit_statistic_by_user(user_id=id)

    context = {
        "user": User.objects.get(id=id),
        "user_commits": user_commits.order_by("-id"),
        "user_total_commits": user_total_commits,
        "user_closed_commits": user_closed_commits,
        "user_undone_commits": user_undone_commits,
        "user_commit_progress_in_percentage": user_commit_progress_in_percentage,
    }
    return render(request, "users/detail.html", context)


# ========== INTERACTORS ==========

def signup(request):
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '').strip()

    User.objects.create_user(
        username=username,
        password=password,
    )
    return redirect('users:login_view')


def login(request):
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '').strip()

    user = authenticate(username=username, password=password)

    if user is None:
        messages.error(request, "These credentials are incorrect")
        return redirect(
            f"{reverse('users:login_view')}"
            f"?username={username}"
        )

    django_login(request, user)
    return redirect('commits:commits_view')


@login_required
def logout(request):
    django_logout(request)
    return redirect('users:login_view')
