from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def index(request):
    return redirect("commits:commits_view")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('commits/', include("apps.commits.urls", namespace="commits")),
    path('users/', include("apps.users.urls", namespace="users")),
]
