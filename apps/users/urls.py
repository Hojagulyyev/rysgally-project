from django.urls import path

from . import views


app_name = 'users'

# Views

urlpatterns = [
    path('signup-view/', views.signup_view, name="signup_view"),
    path('login-view/', views.login_view, name="login_view"),
    path('<int:id>/', views.detail_view, name="detail_view"),
]

# Interactors

urlpatterns += [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
]