from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Strategy, TradeRecord

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
    
class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = ['id', 'name', 'uploaded_at']

class TradeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeRecord
        fields = ['id', 'strategy', 'date', 'entry_price', 'exit_price', 'pnl', 'cumulative_equity']
