from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('income/', views.incomes_view, name='income_list'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('analysis/', views.analysis_view, name='analysis'),
    path('add_income/', views.add_income, name='add_income'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('logout/', views.logout_view, name='logout'),
    path('income/delete/<int:pk>/', views.delete_income, name='delete_income'),
    path('expense/delete/<int:pk>/', views.delete_expense, name='delete_expense'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
