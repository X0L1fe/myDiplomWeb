from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("about/", views.about, name='about'),
    path("register/", views.register, name='register'),
    path("login/", views.loginer, name='login'),
    path('registering/', views.register_view, name='registering'),
    path('logining/', views.login_view, name='logining'),
    path('captcha/', views.captcha_view, name='captcha'),
    # path('success/', views.success_page, name='success'),
    
    # path('profile/', views.profile_view, name='profile'),
    # path('logout/', LogoutView.as_view(), name='logout'),
]