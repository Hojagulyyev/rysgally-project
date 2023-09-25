from django.urls import path

from . import views


app_name = 'users'

urlpatterns = [
    path('signup-view/', views.signup_view, name="signup_view"),
    path('login-view/', views.login_view, name="login_view"),
    path('signup-user/', views.signup_user, name="signup_user"),
    path('login-user/', views.login_user, name="login_user"),
    path('logout-user/', views.logout_user, name="logout_user"),
]
