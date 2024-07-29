from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth

# Create your views here.
def index(request):
    form = login()
    if request.method == "POST":
        form = login(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('adminwindow')
            
    context = {
        'loginform': form
    }

    return render(request, 'registration/login.html', context)

def adminwindow(request):
    return render(request, 'core/admin.html')