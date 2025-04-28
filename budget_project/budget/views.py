from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import IncomeForm, ExpenseForm
from django.db.models import Sum
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
    if request.user.is_authenticated:
        # Доходы и расходы для текущего авторизованного пользователя
        incomes = Income.objects.filter(user=request.user)
        expenses = Expense.objects.filter(user=request.user)

        # Считаем общие суммы
        total_income = sum(income.amount for income in incomes)
        total_expense = sum(expense.amount for expense in expenses)

        # Вычисляем баланс
        balance = total_income - total_expense

        # Передаем данные в шаблон
        return render(request, 'budget/base.html', {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
        })
    else:
        # Для неавторизованных пользователей просто передаем пустые значения
        return render(request, 'budget/base.html', {
            'total_income': 0,
            'total_expense': 0,
            'balance': 0,
        })

def analysis_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    incomes_by_category = Income.objects.filter(user=request.user).values('category__name').annotate(total=Sum('amount'))
    expenses_by_category = Expense.objects.filter(user=request.user).values('category__name').annotate(total=Sum('amount'))

    return render(request, 'budget/analysis.html', {
        'incomes_by_category': incomes_by_category,
        'expenses_by_category': expenses_by_category,
    })

def logout_view(request):
    logout(request)
    return redirect('home')