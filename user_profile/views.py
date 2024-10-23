from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.models import User

@login_required(login_url='login')
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def profile_update(request):
    if request.method == 'POST':
        user = request.user
        user.passport_series = request.POST['passport_series']
        user.passport_number = request.POST['passport_number']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.middle_name = request.POST['middle_name']
        user.phone = request.POST['phone']
        user.save()
        messages.info(request, 'Данные обновлены')
        return redirect('profile')
    return render(request, 'profile.html')
