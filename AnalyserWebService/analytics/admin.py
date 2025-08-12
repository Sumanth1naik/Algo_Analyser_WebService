from django.contrib import admin
from .models import TradeRecord,Strategy # import your model

# Register Strategy
@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'uploaded_at')
    list_filter = ('user', 'name', 'uploaded_at')
    search_fields = ('name', 'user__username')

# Register TradeRecord
@admin.register(TradeRecord)
class TradeRecordAdmin(admin.ModelAdmin):
    list_display = ('strategy', 'date', 'pnl', 'cumulative_equity')
    list_filter = ('strategy', 'date')
    search_fields = ('strategy__name',)
