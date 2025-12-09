from django.urls import path
from .views import CreateItemView

urlpatterns = [
    # Define your API endpoints here
        path('items/', CreateItemView.as_view(), name='create-item')
]