from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('update/', views.profile_update, name='update'),
]