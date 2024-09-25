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
    party_0 = models.ForeignKey(User, related_name='bets_as_party_0', on_delete=models.CASCADE)
    party_1 = models.ForeignKey(User, related_name='bets_as_party_1', on_delete=models.CASCADE)
    arbitrator = models.ForeignKey(User, related_name='arbitrated_bets', null=True, blank=True, on_delete=models.SET_NULL)
    winner = models.ForeignKey(User, related_name='won_bets', null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=[('USD', 'USD'), ('INR','INR')])
    verified_0 = models.BooleanField(default=False)  # Verification by Party 0
    verified_1 = models.BooleanField(default=False)  # Verification by Party 1
    settled = models.BooleanField(default=False)     # Whether the bet is settled
    placed_at = models.DateTimeField(auto_now_add=True)
    settled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Bet: {self.party_0} vs {self.party_1} for {self.amount}"

class Dispute(models.Model):
    bet = models.OneToOneField(Bet, on_delete=models.CASCADE)  # Link each dispute to one bet
    arbitrator = models.ForeignKey(User, related_name='dispute_arbitrations', on_delete=models.CASCADE)
    resolution = models.TextField(blank=True, null=True)  # Optional field to capture dispute resolution

    def __str__(self):
        return f"Dispute for Bet ID {self.bet.id} (Arbitrator: {self.arbitrator.username})"
