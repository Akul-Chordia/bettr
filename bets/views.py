from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required

from .models import Bet , Notification
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from .models import UserWallet
from django.shortcuts import render , redirect
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
            dob = datetime.strptime(dob_str , "%d-%m-%Y").date()
        except ValueError:
            message = "Invalid date format. Please use DD-MM-YYYY."
            return render(request , 'index.html' , {'message': message})

        age = today.year - dob.year - ((today.month , today.day) < (dob.month , dob.day))
        if age < 18:
            message = "User must be at least 18 years old to register."
            return render(request , 'index.html' , {'message': message})

        if User.objects.filter(username=username).exists():
            message = "Username already taken. Please choose another one."
            return render(request , 'index.html' , {'message': message})

        if User.objects.filter(email=email).exists():
            message = "Email already in use. Please choose another one."
            return render(request , 'index.html' , {'message': message})

        user = User.objects.create_user(username=username , first_name=first_name , last_name=last_name , email=email ,
                                        password=password)
        user.save()
        user_wallet = UserWallet(user=user , wallet_balance=wallet_balance)
        user_wallet.save()

        message = f"User {username} created successfully!"
        user = authenticate(request , username=username , password=password)
        if user is not None:
            login(request , user)
            return redirect('index')

        return render(request , 'index.html' , {'message': message})

    return render(request , 'index.html')


def profile_view(request):
    if request.user.is_authenticated:
        return render(request , 'profile.html' , {'user': request.user})
    return redirect('login')  # Redirect to login if not authenticated


def bet_view(request):
    """Render the bet creation page."""
    return render(request , 'bet.html')


def make_bet(request):
    if request.method == 'POST':
        bet_recipient_username = request.POST.get('bet_recipient')
        arbitrator_username = request.POST.get('arbitrator')
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        terms = request.POST.get('terms')
        bet_maker = request.user
        print(1)

        try:
            bet_recipient = User.objects.get(username=bet_recipient_username)
            arbitrator = User.objects.get(username=arbitrator_username)
        except User.DoesNotExist:
            print(2)
            messages.error(request , 'One of the users does not exist.')
            return render(request , 'bet.html' , {
                'bet_recipient': bet_recipient_username ,
                'arbitrator': arbitrator_username ,
                'amount': amount ,
                'currency': currency ,
                'terms': terms ,
            })

        bet = Bet.objects.create(
            bet_maker=bet_maker ,
            bet_recipient=bet_recipient ,
            arbitrator=arbitrator ,
            amount=amount ,
            currency=currency ,
            verified_0=False ,
            verified_1=False ,
            settled=False ,
            placed_at=datetime.now() ,
            terms=terms
        )
        bet.save()

        Notification.objects.create(
            user_to=bet_recipient ,
            notification_type='bet_invite' ,
            bet=bet ,
            is_read=False
        )

        messages.success(request ,
                         f"Bet created between {bet_maker.username} and {bet_recipient.username} for {amount} {currency}.")
        return redirect('index')

    return render(request , 'bet.html')


def validate_bet(request):
    return 0


def add_money(request):
    return 0


def transaction(request):
    return 0
