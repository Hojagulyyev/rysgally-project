from django.urls import path

from . import views


app_name = 'commits'

urlpatterns = [
    path('', views.commits_view, name="commits_view"),
    path('<int:id>/', views.commit_detail_view, name="detail_view"),
    path('<int:id>/update/', views.update_commit, name="update"),
]
