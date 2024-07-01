from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from core.models import Customer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'account/Login.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from core.models import Customer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError               

def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone_field')

        if password == confirm_password:
            try:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists.")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists.")
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    data = Customer(user=user, phone_field=phone)
                    data.save()
                    our_user = authenticate(username=username, password=password)
                    if our_user is not None:
                        login(request, user)
                        return redirect('/')
            except IntegrityError as e:
                messages.error(request, "Error creating user. Please try again later.")
                # Log the exception for debugging
                print(e)
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'account/register.html')


def user_logout(request):
    logout(request)
    return redirect('/')
