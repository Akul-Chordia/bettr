from django.shortcuts import render
from django.contrib.auth.models import User
from .models import UserProfile
def index(request):
    return render(request, 'index.html')

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
