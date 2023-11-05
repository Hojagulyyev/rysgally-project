from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Prefetch, Sum
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from rysgally_project.settings import (
    COMMIT_BODY_MIN_LENGTH,
    MAX_COMMIT_BONUS,
    MY_COMMITS_PAGE_SIZE,
    OTHER_COMMITS_PAGE_SIZE,
)

from .models import Commit
from .services import get_commit_statistic_by_user


# ========== VIEWS ==========
@login_required
def commits_view(request):
    username = request.GET.get("username", "")

    (
        user_commits,
        user_total_commits,
        user_total_bonus,
        user_closed_commits,
        user_undone_commits,
        user_commit_progress_in_percentage,
    ) = get_commit_statistic_by_user(request.user.id)

    other_users = (
        User.objects.exclude(id=request.user.id)
        .filter(username__icontains=username)
        .prefetch_related(
            Prefetch(
                "commit_set",
                queryset=Commit.objects.order_by("-id")[:OTHER_COMMITS_PAGE_SIZE],
                to_attr="recent_commits",
            )
        )
        .annotate(
            commit_count=Count("commit"),
            total_bonus=Sum("commit__bonus"),
        )
    )

    context = {
        "my_commits": user_commits.order_by("-id")[:MY_COMMITS_PAGE_SIZE],
        "my_total_commits": user_total_commits,
        "my_total_bonus": user_total_bonus,
        "my_closed_commits": user_closed_commits,
        "my_undone_commits": user_undone_commits,
        "my_commit_progress_in_percentage": user_commit_progress_in_percentage,
        "other_users": other_users,
    }
    return render(request, "commits/index.html", context)


@login_required
def detail_view(request, id: int):
    commit = Commit.objects.get(id=id)

    context = {
        "commit": commit,
    }
    return render(request, "commits/detail.html", context)


# ========== INTERACTORS ==========
@login_required
def update(request, id: int):
    commit = Commit.objects.get(id=id)
    body = request.POST.get("body", "").strip()

    # ========== VALIDATION ==========

    if not commit.user == request.user:
        messages.error(request, "You aren't author of commit")
        return redirect("commits:commits_view")

    if len(body) < COMMIT_BODY_MIN_LENGTH or len(body) < len(commit.body):
        messages.error(
            request, f"commit body is less than {COMMIT_BODY_MIN_LENGTH} or older body"
        )
        return redirect(
            f"{reverse('commits:detail_view', kwargs={'id': id})}" f"?body={body}"
        )

    # ========== PROCESS ==========

    days_difference = (timezone.now() - commit.created_datetime).days

    if days_difference in range(MAX_COMMIT_BONUS):
        current_bonus = MAX_COMMIT_BONUS - days_difference
        if current_bonus > commit.bonus:
            commit.bonus += current_bonus

    commit.body = body
    commit.save(update_fields=["body", "bonus"])

    return redirect("commits:commits_view")
