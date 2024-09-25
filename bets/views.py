from django.contrib.auth.models import User
from .models import UserWallet
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login
from django.contrib import messages


def index(request):
    return render(request , 'index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request , username=username , password=password)
        if user is not None:
            login(request , user)
            return redirect('index')  # Redirect to the home page or index
        else:
            messages.error(request , 'Invalid username or password')
    return render(request , 'index.html')  # Render the index page for GET requests


def create_user_profile():

    email = input("Enter email: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    dob = input("Enter date of birth (DD-MM-YYYY): ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    wallet_balance = 0.00

    user = User.objects.create_user(username=username , first_name=first_name , last_name=last_name , email=email ,
                                    password=password)
    user.save()

    user_wallet = UserWallet(user=user , wallet_balance=wallet_balance)
    user_wallet.save()

    print(f"User {username} created successfully with ID: {user.id}!")
