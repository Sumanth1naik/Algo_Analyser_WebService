from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Strategy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to logged-in user
    name = models.CharField(max_length=100)                   # Strategy name (e.g., Momentum_MA)
    uploaded_at = models.DateTimeField(auto_now_add=True)     # Auto timestamp when file is uploaded

    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
class TradeRecord(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE, related_name='trades')  # Links to Strategy
    date = models.DateField()
    entry_price = models.FloatField()
    exit_price = models.FloatField()
    pnl = models.FloatField()
    cumulative_equity = models.FloatField()

    def __str__(self):
        return f"{self.strategy.name} - {self.date} (PnL: {self.pnl})"

