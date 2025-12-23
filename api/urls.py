from django.urls import path
from .views import CreateItemView, MovementLogView, InboundStockView

urlpatterns = [
    # Define your API endpoints here
        path('items/', CreateItemView.as_view(), name='create-item'),
        path('movements/', MovementLogView.as_view(), name='log-movement'),
        path('inbound/', InboundStockView.as_view(), name='inbound-stock'),
]