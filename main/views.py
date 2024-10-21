from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.functional import SimpleLazyObject
from .forms import *
import random
import string
from captcha.image import ImageCaptcha
from django.conf import settings
import os
from django.contrib.auth import get_user_model

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    return render(request, 'register.html')

def register_view(request):
    if request.method == 'POST':
        user_login = request.POST['login']
        email = request.POST['email']
        password = request.POST['password']
        password_repeat = request.POST['password_repeat']

        # Проверка на совпадение паролей
        if password != password_repeat:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'register.html')

        # Проверка, существует ли пользователь с таким логином
        if User.objects.filter(login=user_login).exists():
            messages.error(request, 'Пользователь с таким логином уже существует')
            return render(request, 'register.html')

        # Проверка, существует ли пользователь с таким email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return render(request, 'register.html')

        # Создание пользователя
        user = User.objects.create_user(login=user_login, email=email, password=password)
        user.save()

        # Вход пользователя после регистрации
        user = authenticate(request, login=user_login, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Перенаправляем на домашнюю страницу после успешной регистрации
        else:
            messages.error(request, 'Не удалось зайти в аккаунт')
            return redirect('login')
    return render(request, 'register.html')

def loginer(request):
    return render(request, 'login.html')

def login_view(request):
    login_attempts = request.session.get('login_attempts', 0)

    if request.method == 'POST':
        user_login = request.POST['login']
        password = request.POST['password']

        User = get_user_model()  # Получаем модель пользователя
        try:
            user = User.objects.get(login=user_login)  # Ищем пользователя по логину
        except User.DoesNotExist:
            messages.error(request, 'Неверные логин или пароль')
            login_attempts += 1
            request.session['login_attempts'] = login_attempts
            return render(request, 'login.html', {'show_captcha_modal': False})

        if user.check_password(password):  # Проверяем пароль
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему!')
            request.session['login_attempts'] = 0  # Сброс счетчика попыток
            return redirect('home')
        else:
            login_attempts += 1
            request.session['login_attempts'] = login_attempts  # Увеличиваем количество попыток
            messages.error(request, 'Неверные логин или пароль')

            if login_attempts >= 3:
                captcha_image_url = generate_captcha(request)  # Генерация CAPTCHA
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

    # Генерация новой CAPTCHA
    captcha_image_url = generate_captcha(request)
    return render(request, 'captcha.html', {'captcha_image_url': captcha_image_url, 'show_captcha_modal': True})


def generate_captcha(request):
    captcha_text = ''.join(random.choices(string.ascii_letters + string.digits, k=6))  # Генерация текста
    request.session['captcha_text'] = captcha_text  # Сохранение текста CAPTCHA в сессии
    print(captcha_text)
    image = ImageCaptcha(width=300, height=100)
    image_name = 'captcha.png'
    image_path = os.path.join(settings.STATICFILES_DIRS[0], 'captcha', image_name)  # Сохранение в static/captcha
    image.write(captcha_text, image_path)

    return settings.STATIC_URL + 'captcha/' + image_name

@login_required
def profile_view(request):
    # Сообщение об успешном входе
    messages.success(request, f'Добро пожаловать, {request.user.login}!')

    return render(request, 'profile.html')

def logout_view(request):
    logout(request)
    messages.info(request, f'Вы вышли из аккаунта.') 
    return redirect('home')