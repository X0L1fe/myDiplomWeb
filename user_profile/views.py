from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def profile_view(request):
    # Сообщение об успешном входе
    messages.success(request, f'Добро пожаловать, {request.user.login}!')

    return render(request, 'profile.html')
