from django.contrib.auth.models import User
from django.db import models

class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    user_from = models.ForeignKey(User, related_name='transactions_sent', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='transactions_received', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bet = models.ForeignKey('Bet', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])

    def __str__(self):
        return f"{self.user_from} -> {self.user_to}: {self.amount} (Bet ID: {self.bet.id})"


class Bet(models.Model):
    bet_maker = models.ForeignKey(User, related_name='betting_side', on_delete=models.CASCADE, default=1)
    bet_recipient = models.ForeignKey(User, related_name='bet_opposing_side', on_delete=models.CASCADE, default=1)
    bet_active = models.BooleanField(default=False)
    arbitrator = models.ForeignKey(User, related_name='arbitrated_bets', null=True, blank=True, on_delete=models.SET_NULL)
    winner = models.ForeignKey(User, related_name='won_bets', null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=[('USD', 'USD'), ('INR','INR')])
    terms = models.TextField(default="terms and conditions")
    verified_0 = models.BooleanField(default=False)
    verified_1 = models.BooleanField(default=False)
    settled = models.BooleanField(default=False)
    placed_at = models.DateTimeField(auto_now_add=True)
    settled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Bet: {self.bet_maker} vs {self.bet_recipient} for {self.amount}"

class Dispute(models.Model):
    bet = models.OneToOneField(Bet, on_delete=models.CASCADE)
    arbitrator = models.ForeignKey(User, related_name='dispute_arbitrations', on_delete=models.CASCADE)
    resolution = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Dispute for Bet ID {self.bet.id} (Arbitrator: {self.arbitrator.username})"
