from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from captcha.image import ImageCaptcha
from .forms import *
from .models import User, UserProfile
from .serializers import UserProfileSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
import random
import string
import os

class UserAPI(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = [TokenAuthentication]  # Указываем, что используем токен-аутентификацию
    permission_classes = [IsAdminUser]



def register(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'register.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        user_login = request.POST['login']
        email = request.POST['email']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']

        if password != password_repeat:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'register.html')

        if User.objects.filter(login=user_login).exists():
            messages.error(request, 'Пользователь с таким логином уже существует')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return render(request, 'register.html')

        user = User.objects.create_user(login=user_login, email=email, password=password)
        user.save()

        user = authenticate(request, login=user_login, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Не удалось зайти в аккаунт')
            return redirect('login')
    return render(request, 'register.html')

def loginer(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'login.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    login_attempts = request.session.get('login_attempts', 0)

    if request.method == 'POST':
        user_login = request.POST['login']
        password = request.POST['password']

        User = get_user_model()
        try:
            user = User.objects.get(login=user_login)
        except User.DoesNotExist:
            messages.error(request, 'Неверные логин или пароль')
            login_attempts += 1
            request.session['login_attempts'] = login_attempts
            return render(request, 'login.html', {'show_captcha_modal': False})

        if user.check_password(password):
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему!')
            request.session['login_attempts'] = 0
            return redirect('home')
        else:
            login_attempts += 1
            request.session['login_attempts'] = login_attempts
            messages.error(request, 'Неверные логин или пароль')

            if login_attempts >= 3:
                captcha_image_url = generate_captcha(request)
                return render(request, 'login.html', {
                    'show_captcha_modal': True, 
                    'captcha_image_url': captcha_image_url
                })

    return render(request, 'login.html', {'show_captcha_modal': False})

def captcha_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('captcha_input')

        # Проверяем текст CAPTCHA
        if user_input and user_input == request.session.get('captcha_text', ''):
            request.session['login_attempts'] = 0  # Сброс попыток
            messages.success(request, 'Капча введена верно!')
            return redirect('logining')  # Возвращаемся на страницу логина
        else:
            messages.error(request, 'Капча введена неверно. Попробуйте снова.')

    captcha_image_url = generate_captcha(request)
    return render(request, 'captcha.html', {'captcha_image_url': captcha_image_url, 'show_captcha_modal': True})


def generate_captcha(request):
    captcha_text = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    request.session['captcha_text'] = captcha_text
    print(captcha_text)
    image = ImageCaptcha(width=300, height=100)
    image_name = 'captcha.png'
    image_path = os.path.join(settings.STATICFILES_DIRS[0], 'captcha', image_name)
    image.write(captcha_text, image_path)

    return settings.STATIC_URL + 'captcha/' + image_name

@login_required(login_url='home')
def logout_view(request):
    logout(request)
    messages.info(request, f'Вы вышли из аккаунта.') 
    return redirect('home')

@login_required(login_url='login')
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def profile_update(request):
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        
        profile.passport_series = request.POST.get('passport_series')
        profile.passport_number = request.POST.get('passport_number')
        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.middle_name = request.POST.get('middle_name')
        profile.phone = request.POST.get('phone')
        
        profile.save()
        messages.info(request, 'Данные обновлены')
        return redirect('profile')
    return render(request, 'profile.html')
