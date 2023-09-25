from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def index(request):
    return redirect("commits:commits_view")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('rysgally-project/', index),
    path('rysgally-project/commits/', include("apps.commits.urls", namespace="commits")),
    path('rysgally-project/users/', include("apps.users.urls", namespace="users")),
]
