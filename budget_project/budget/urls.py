from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('income/', views.income_list, name='income_list'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('analysis/', views.analysis_view, name='analysis'),
    path('add_income/', views.add_income, name='add_income'),
    path('add_expense/', views.add_expense, name='add_expense'),
]
