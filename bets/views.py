from datetime import datetime
from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render , redirect
from django.utils import timezone

from .models import Bet , Notification , UserWallet , Transaction

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def index(request):
    return render(request , 'index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request , username=username , password=password)
        if user is not None:
            login(request , user)
            return redirect('index')
        else:
            messages.error(request , 'Invalid username or password')
    return render(request , 'index.html')


def logout_view(request):
    logout(request)
    return redirect('index')


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
        user_wallet = UserWallet.objects.create(user_id=user.id , wallet_balance=wallet_balance, on_hold_balance=0.00)
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
    return redirect('login')


def bet_view(request):
    return render(request , 'bet.html')


def make_bet(request):
    if request.method == 'POST':
        bet_recipient_username = request.POST.get('bet_recipient')
        arbitrator_username = request.POST.get('arbitrator')
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        terms = request.POST.get('terms')
        bet_maker = request.user
        amount = Decimal(amount)
        try:
            bet_recipient = User.objects.get(username=bet_recipient_username)
            arbitrator = User.objects.get(username=arbitrator_username)
        except User.DoesNotExist:
            messages.error(request , 'One of the users does not exist.')
            return render(request , 'bet.html' , {
                'bet_recipient': bet_recipient_username ,
                'arbitrator': arbitrator_username ,
                'amount': amount ,
                'currency': currency ,
                'terms': terms ,
            })
        user_wallet = UserWallet.objects.get(user_id=request.user)
        if user_wallet.wallet_balance < amount:
            messages.error(request , 'Bet amount must be less than than wallet amount.')
            return render(request , 'bet.html' , {
                'bet_recipient': bet_recipient_username ,
                'arbitrator': arbitrator_username ,
                'amount': Decimal('0') ,
                'currency': currency ,
                'terms': terms ,
            })
        else:
            user_wallet.wallet_balance -= amount
            user_wallet.on_hold_balance += amount
            user_wallet.save()
        bet = Bet.objects.create(
            bet_maker=bet_maker ,
            bet_recipient=bet_recipient ,
            arbitrator=arbitrator ,
            amount=amount ,
            currency=currency ,
            settled=False ,
            placed_at=datetime.now() ,
            terms=terms
        )
        bet.save()
        bet_notification = Notification.objects.create(
            user_to=bet_recipient ,
            notification_type='bet_invite' ,
            bet_id=bet.id ,
            created_at=datetime.now() ,
            is_read=False
        )

        bet_notification.save()

        messages.success(request ,
                         f"Bet created between {bet_maker.username} and {bet_recipient.username} for {amount} {currency}.")

    return render(request , 'bet.html')


def validate_bet(request):
    if request.method == 'POST':
        outcome = request.POST.get('outcome')
        bet_id = request.POST.get('bet')
        notification_id = request.POST.get('notification_id')
        print(1)

        bet = Bet.objects.get(id=bet_id)
        user_wallet = UserWallet.objects.get(user_id=request.user)
        sender_wallet = UserWallet.objects.get(user_id=bet.bet_maker)
        notification = Notification.objects.get(id=notification_id)
        if outcome == '1':
            if user_wallet.wallet_balance < bet.amount:
                messages.error(request , 'Bet amount must be less than than wallet amount.')
                return render(request , 'wallet.html')
            else:
                user_wallet.wallet_balance -= bet.amount
                user_wallet.on_hold_balance += bet.amount
                user_wallet.save()
                transfer(bet.bet_maker_id , 1 , bet.amount , bet.id)
                transfer(bet.bet_recipient_id , 1 , bet.amount , bet.id)
                bet.bet_active = True
                bet.save()
                notification.is_read = True
                notification.save()
        elif outcome == '0':
            bet.delete()
            sender_wallet.on_hold_balance -= bet.amount
            sender_wallet.wallet_balance += bet.amount
            sender_wallet.save()
            notification.is_read = True
            notification.save()
    return render(request , 'index.html')


def claim_dispute(request):
    if request.method == 'POST':
        outcome = request.POST.get('outcome')
        bet_id = request.POST.get('bet')
        notification_id = request.POST.get('notification_id')
        bet = Bet.objects.get(id=bet_id)
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()

        if outcome == 1:
            if request.user == bet.bet_maker:
                bet.winner_id = bet.bet_recipient
                bet.save()
            elif request.user == bet.bet_recipient:
                bet.winner_id = bet.bet_maker
                bet.save()
            else:
                messages.error('Something went wrong')
                return render(request , 'index.html')
            transfer(1 , bet.winner , bet.amount * 2 , bet_id)

        elif outcome == 0:
            bet_notification = Notification.objects.create(
                user_to_id=bet.arbitrator ,
                notification_type='arbitration_request' ,
                user_from_id=request.user ,
                bet_id=bet.id ,
                created_at=datetime.now() ,
                is_read=False
            )
            bet_notification.save()

    return 0


def arbitrator_rule(request):
    if request.method == 'POST':
        outcome = request.POST.get('outcome')
        bet_id = request.POST.get('bet')
        notification_id = request.POST.get('notification_id')
        bet = Bet.objects.get(id=bet_id)
        notification = Notification.objects.filter(id=notification_id)
        notification.is_read = True
        notification.save()

        if outcome == -1:
            bet.winner = bet.bet_maker
            bet.save()
            transfer(1 , bet.winner , bet.amount * 2 , bet_id)
        elif outcome == 0:
            transfer(1 , bet.bet_maker , bet.amount , bet_id)
            transfer(1 , bet.bet_recipient , bet.amount , bet_id)
            bet.delete()
        elif outcome == 1:
            bet.winner = bet.bet_recipient
            bet.save()
            transfer(1 , bet.winner , bet.amount * 2 , bet_id)
    return 0


def add_money(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        card_number = request.POST.get('card_number')
        card_expiry = request.POST.get('card_expiry')
        card_cvc = request.POST.get('card_cvc')

        exp_month , exp_year = card_expiry.split('/')
        exp_month = int(exp_month)
        exp_year = int(exp_year) + 2000

        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

        try:
            token = stripe.Token.create(
                card={
                    "number": card_number ,
                    "exp_month": exp_month ,
                    "exp_year": exp_year ,
                    "cvc": card_cvc ,
                }
            )

            charge = stripe.Charge.create(
                amount=int(float(amount) * 100) ,
                currency="usd" ,
                source=token.id ,
                description="Add money to wallet"
            )

            charge.save()

            user_wallet = UserWallet.objects.get(user=request.user)
            user_wallet.wallet_balance += Decimal(amount)
            user_wallet.save()

            messages.success(request , 'Money added successfully!')
        except Exception as e:
            messages.error(request , f'There was an error processing your payment: {str(e)}')

    return redirect('wallet')


def withdraw_money(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        amount = Decimal(amount)
        user_wallet = UserWallet.objects.get(user_id=request.user)
        if user_wallet.wallet_balance >= amount:
            user_wallet.wallet_balance -= amount
            user_wallet.save()
        else:
            messages.error(request , 'You don\'t have that much money brokie')
    return redirect('wallet')


def claim_bet(request):
    if request.method == 'POST':
        bet_id = request.POST.get('bet')
        bet = Bet.objects.get(id=bet_id)

        if request.user == bet.bet_maker:
            claimer = bet.bet_recipient
        elif request.user == bet.bet_recipient:
            claimer = bet.bet_maker
        else:
            messages.error(request , 'idk wtf went wrong you\'re never supposed to reach here')
            return redirect('index.html')

        bet_notification = Notification.objects.create(
            user_to=claimer ,
            notification_type='claim_verification' ,
            bet_id=bet.id ,
            created_at=datetime.now() ,
            is_read=False
        )

        bet_notification.save()
    return 0


def transfer(sender_id , receiver_id , amount , bet_id):
    sender_waller = UserWallet.objects.get(user_id=sender_id)
    receiver_wallet = UserWallet.objects.get(user_id=receiver_id)
    amount = Decimal(amount)
    transaction = Transaction.objects.create(
        user_from_id=sender_id ,
        user_to_id=receiver_id ,
        timestamp=datetime.now() ,
        amount=amount ,
        bet_id=bet_id ,
        status=False
    )
    transaction.save()

    try:
        sender_waller.on_hold_balance -= amount
        receiver_wallet.on_hold_balance += amount
        transaction.status = True
        sender_waller.save()
        receiver_wallet.save()
    except:
        messages.error('TRANSACTION FAILED')
    return 0


@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()

        return redirect('index')

    return render(request , 'profile.html')


@login_required
def my_bets_view(request):
    user = request.user
    my_bets = Bet.objects.filter(bet_maker=user) | Bet.objects.filter(bet_recipient=user)
    my_bets = my_bets.distinct()

    context = {
        'my_bets': my_bets ,
    }
    return render(request , 'my_bets.html' , context)


@login_required
def wallet(request):
    user_wallet = UserWallet.objects.get(user=request.user)
    return render(request , 'wallet.html' , {'user_wallet': user_wallet})


def notification_view(request):
    notifications = Notification.objects.filter(user_to=request.user , is_read=False)
    bets = {notification.bet_id: Bet.objects.get(id=notification.bet_id) for notification in notifications}
    return render(request , 'index.html' , {'notifications': notifications , 'bets': bets})
