from django.urls import path
from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard-page"), # Home page
    path("configure/", views.ConfigureView.as_view(), name="configure-page"), # Configuration page
]