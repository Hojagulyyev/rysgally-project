from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models.functions import Length
from django.db.models import Q, Prefetch, Count
from django.contrib.auth.models import User
from django.contrib import messages

from rysgally_project.settings import (
    COMMIT_BODY_MIN_LENGTH,
    MY_COMMITS_PAGE_SIZE,
    OTHER_COMMITS_PAGE_SIZE,
)
from .models import Commit


# ========== VIEWS ==========

@login_required
def commits_view(request):
    my_commits = Commit.objects.filter(user=request.user).annotate(body_len=Length("body"))
    total_commits = my_commits.count()
    closed_commits = my_commits.filter(body_len__gte=COMMIT_BODY_MIN_LENGTH).count()
    undone_commits = my_commits.filter(
        Q(body=None)
        | Q(body_len__lt=COMMIT_BODY_MIN_LENGTH)
    ).count()
    commit_progress_in_percentage = (closed_commits / total_commits) * 100

    users = User.objects \
        .exclude(id=request.user.id) \
        .prefetch_related(
            Prefetch(
                'commit_set',
                queryset=Commit.objects.order_by('-id')[:OTHER_COMMITS_PAGE_SIZE],
                to_attr='recent_commits'
            )
        ) \
        .annotate(commit_count=Count('commit'))

    context = {
        "my_commits": my_commits.order_by("-id")[:MY_COMMITS_PAGE_SIZE],
        "users": users,
        "total_commits": total_commits,
        "closed_commits": closed_commits,
        "undone_commits": undone_commits,
        "commit_progress_in_percentage": round(commit_progress_in_percentage, 1)
    }
    return render(request, "commits/index.html", context)


@login_required
def detail_view(request, id: int):
    commit = Commit.objects.get(id=id)

    # ========== VALIDATION ==========

    context = {
        "commit": commit,
    }
    return render(request, "commits/detail.html", context)


# ========== INTERACTORS ==========

@login_required
def update(request, id: int):
    commit = Commit.objects.get(id=id)
    body = request.POST.get("body", "")

    # ========== VALIDATION ==========

    if not commit.user == request.user:
        messages.error(request, "You aren't author of commit")
        return redirect("commits:commits_view")

    if len(body) < COMMIT_BODY_MIN_LENGTH:
        messages.error(request, f"commit body is less than {COMMIT_BODY_MIN_LENGTH} character")
        return redirect(
            f"{reverse('commits:detail_view', kwargs={'id': id})}"
            f"?body={body}"
        )

    # ========== PROCESS ==========

    commit.body = body
    commit.save(update_fields=["body"])

    return redirect('commits:commits_view')
