from django.urls import path
from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard-page"), # Home page
    path("configure/", views.ConfigureView.as_view(), name="configure-page"), # Configuration page
    path("item_lookup/", views.ItemsLookupView.as_view(), name="item-lookup-page"), # Item list page
    path("problem_solve/", views.ProblemSolveView.as_view(), name="problem-solve-page"), # Problem solve page
]