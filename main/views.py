from django.shortcuts import render, redirect

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contacts(request):
    return render(request, 'contacts.html')

def documents(request):
    return render(request, 'documents.html')

