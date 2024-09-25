from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from .models import UserWallet
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the home page or index
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'index.html')  # Render the index page for GET requests

def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to the home page after logout

def create_user_profile(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        dob_str = request.POST.get('dob')
        username = request.POST.get('username')
        password = request.POST.get('password')

        wallet_balance = 0.00
        today = timezone.now().date()

        try:
            dob = datetime.strptime(dob_str, "%d-%m-%Y").date()
        except ValueError:
            return {"error": "Invalid date format. Please use DD-MM-YYYY."}

        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            return {"error": "User must be at least 18 years old to register."}

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                        password=password)
        user.save()
        user_wallet = UserWallet(user=user, wallet_balance=wallet_balance)
        user_wallet.save()

        print(f"User {username} created successfully with ID: {user.id}!")
        return redirect('index')  # Redirect to the home page after successful registration

    return render(request, 'index.html')  # Render the index page for GET requests

def profile_view(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html', {'user': request.user})
    return redirect('login')  # Redirect to login if not authenticated

def make_bet(request):
    return 0

def validate_bet(request):
    return 0

def add_money(request):
    return 0


def transaction(request):
    return 0