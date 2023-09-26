from django.urls import path

from . import views


app_name = 'commits'

# Views

urlpatterns = [
    path('', views.commits_view, name="commits_view"),
    path('<int:id>/', views.detail_view, name="detail_view"),
]

# Interactors

urlpatterns += [
    path('<int:id>/update/', views.update, name="update"),
]
