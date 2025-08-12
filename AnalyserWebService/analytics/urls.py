from django.urls import path
from .views import Home,StrategyUploadView,StrategyListView,TradeRecordListView



urlpatterns = [
    path('', Home.as_view()),
    path('upload-strategy/', StrategyUploadView.as_view(), name='upload-strategy'),
    path('strategies/', StrategyListView.as_view(), name='strategy-list'),
    path('strategies/<int:strategy_id>/trades/', TradeRecordListView.as_view(), name='trade-list'),
]