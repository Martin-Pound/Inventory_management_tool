from django.urls import path
from .views import CreateItemView, MovementLogView

urlpatterns = [
    # Define your API endpoints here
        path('items/', CreateItemView.as_view(), name='create-item'),
        path('movements/', MovementLogView.as_view(), name='log-movement')

]