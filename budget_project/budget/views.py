from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import IncomeForm, ExpenseForm
from .models import Income, Expense, IncomeCategory, ExpenseCategory

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'budget/register.html', {'form': form})


def income_list(request):
    incomes = Income.objects.filter(user=request.user)
    return render(request, 'budget/income_list.html', {'incomes': incomes})

def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'budget/expense_list.html', {'expenses': expenses})


def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # Присваиваем текущего пользователя
            income.save()
            return redirect('home')
    else:
        form = IncomeForm()
    return render(request, 'budget/add_income.html', {'form': form})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Присваиваем текущего пользователя
            expense.save()
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'budget/add_expense.html', {'form': form})

def home(request):
    return render(request, 'budget/base.html')

def analysis_view(request):
    return render(request, 'budget/analysis.html')

