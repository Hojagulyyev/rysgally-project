from django.db.models import Q
from django.db.models.functions import Length

from rysgally_project.settings import (
    COMMIT_BODY_MIN_LENGTH,
    ROUND_DECIMAL_PLACES,
)
from .models import Commit


def get_commit_statistic_by_user(user_id: int):
    user_commits = Commit.objects.filter(user_id=user_id).annotate(body_len=Length("body"))
    user_total_commits = user_commits.count()
    user_closed_commits = user_commits.filter(body_len__gte=COMMIT_BODY_MIN_LENGTH).count()
    user_undone_commits = user_commits.filter(
        Q(body=None) | Q(body_len__lt=COMMIT_BODY_MIN_LENGTH)
    ).count()
    user_commit_progress_in_percentage = round(
        (user_closed_commits / user_total_commits) * 100,
        ROUND_DECIMAL_PLACES,
    )
    return (
        user_commits,
        user_total_commits,
        user_closed_commits,
        user_undone_commits,
        user_commit_progress_in_percentage,
    )
