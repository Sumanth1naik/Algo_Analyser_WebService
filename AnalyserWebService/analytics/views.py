import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .serializers import RegisterSerializer,StrategySerializer,TradeRecordSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework import status, permissions
from .models import Strategy, TradeRecord



class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
    
    
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token or already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)
        
        

class StrategyUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        strategy_name = request.data.get('strategy_name')
        csv_file = request.FILES.get('file')

        if not strategy_name or not csv_file:
            return Response({'error': 'Missing strategy name or file.'}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Create or get existing strategy
        strategy, created = Strategy.objects.get_or_create(user=request.user, name=strategy_name)

        # Step 2: Parse the CSV using pandas
        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            return Response({'error': 'Invalid CSV format.'}, status=status.HTTP_400_BAD_REQUEST)

        # Step 3: Loop through rows and create TradeRecords
        for _, row in df.iterrows():
            TradeRecord.objects.create(
                strategy=strategy,
                date=row['Date'],
                entry_price=row['Entry Price'],
                exit_price=row['Exit Price'],
                pnl=row['PnL'],
                cumulative_equity=row['Cumulative Equity']
            )

        return Response({'message': 'Strategy uploaded successfully.'}, status=status.HTTP_201_CREATED)


class StrategyListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        strategies = Strategy.objects.filter(user=user).order_by('-uploaded_at')
        serializer = StrategySerializer(strategies, many=True)
        return Response(serializer.data)



class TradeRecordListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, strategy_id):
        try:
            strategy = Strategy.objects.get(id=strategy_id, user=request.user)
        except Strategy.DoesNotExist:
            return Response({'error': 'Strategy not found'}, status=status.HTTP_404_NOT_FOUND)

        trades = TradeRecord.objects.filter(strategy=strategy).order_by('date')
        serializer = TradeRecordSerializer(trades, many=True)
        return Response(serializer.data)