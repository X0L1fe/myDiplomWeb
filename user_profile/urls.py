from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import UserAPI
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path("register/", views.register, name='register'),
    path("login/", views.loginer, name='login'),
    path('registering/', views.register_view, name='registering'),
    path('logining/', views.login_view, name='logining'),
    path('captcha/', views.captcha_view, name='captcha'),
    path('logout/', views.logout_view, name='logout'),
    path('update/', views.profile_update, name='update'),
    path('api/accounts/list/', UserAPI.as_view(), name='api_account')
]