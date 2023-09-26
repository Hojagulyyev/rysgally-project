from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from rysgally_project.settings import NGINX_PRELOCATION


def index(request):
    return redirect("commits:commits_view")


urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{NGINX_PRELOCATION}/", index),
    path(f"{NGINX_PRELOCATION}/commits/", include("apps.commits.urls", namespace="commits")),
    path(f"{NGINX_PRELOCATION}/users/", include("apps.users.urls", namespace="users")),
]
