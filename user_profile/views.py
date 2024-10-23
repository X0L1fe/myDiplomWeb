from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def profile_view(request):
    # Сообщение об успешном входе
    messages.success(request, f'Добро пожаловать, {request.user.login}!')

    return render(request, 'profile.html')

@login_required
def profile_update(request):
    if request.method == 'POST':
        user = request.user
        user.passport = request.POST['passport']
        user.first_name = request.POST['firs_name']
        user.last_name = request.POST['last_name']
        user.middle_name = request.POST['middle_name']
        user.phone = request.POST['phone']
        user.save()
        return redirect('profile')  # Перенаправляем обратно на страницу профиля
    return render(request, 'profile.html')
