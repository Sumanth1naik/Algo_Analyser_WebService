from django.db import models

# Create your models here.

class TradeRecord(models.Model):
    date = models.DateField()
    strategy = models.CharField(max_length=100)
    entry_price = models.FloatField()
    exit_price = models.FloatField()
    pnl = models.FloatField()
    cumulative_equity = models.FloatField()

