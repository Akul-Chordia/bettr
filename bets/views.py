from django.shortcuts import render
from django.contrib.auth.models import User
from .models import UserProfile
def index(request):
    return render(request, 'index.html')

def create_user_profile():
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    dob = input("Enter date of birth (DD-MM-YYYY): ")
    wallet_balance = 0.00

    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()


    user_profile = UserProfile(user=user, dob=dob, wallet_balance=wallet_balance)
    user_profile.save()

    print(f"User {username} created successfully with ID: {user.id}!")
