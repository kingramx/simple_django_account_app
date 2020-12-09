from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import auth



def register_view(request):

    if request.method == 'POST':
        first_name = 'No FirstName'
        last_name = 'No LastName'
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        conf_password = request.POST['conf_password']
        
        if password == conf_password:
            if User.objects.filter(username=username).exists():
                print("This username is taken before!")
                return redirect('register')
            else:
                if User.objects.filter(email=email):
                    print("This emal is taken before!")
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username,
                                                    password=password,
                                                    email = email)
                    user.save()
                    print("User registered successfully!")
                    return redirect('login')
        else:
            print("Passwrods do not match, Try again!")
            return redirect('register')
    else:
        return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            print('You are now logged in')
            return redirect('dashboard')
        else:
            print('Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')