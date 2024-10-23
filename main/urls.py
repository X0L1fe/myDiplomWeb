from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("about/", views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('documents/', views.documents, name='documents'),
    path("register/", views.register, name='register'),
    path("login/", views.loginer, name='login'),
    path('registering/', views.register_view, name='registering'),
    path('logining/', views.login_view, name='logining'),
    path('captcha/', views.captcha_view, name='captcha'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    # path('success/', views.success_page, name='success'),
    
]