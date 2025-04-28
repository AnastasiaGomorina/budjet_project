from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import IncomeForm, ExpenseForm, PeriodForm
from django.db.models import Sum
from .models import Income, Expense, IncomeCategory, ExpenseCategory
from django.contrib.auth.decorators import login_required
from datetime import date


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


@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)  # ещё не сохраняем в базу
            income.user = request.user        # подставляем текущего пользователя
            income.save()                     # теперь сохраняем
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'budget/add_income.html', {'form': form})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
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

    form = PeriodForm(request.GET)

    if form.is_valid():
        # Извлекаем значения из формы
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        # Фильтруем по датам
        incomes = Income.objects.filter(user=request.user, date__range=[start_date, end_date])
        expenses = Expense.objects.filter(user=request.user, date__range=[start_date, end_date])

        print(f"Start Date: {start_date}, End Date: {end_date}")  # Для отладки

        # Группируем по категориям и вычисляем сумму
        incomes_by_category = incomes.values('category__name').annotate(total=Sum('amount'))
        expenses_by_category = expenses.values('category__name').annotate(total=Sum('amount'))

        return render(request, 'budget/analysis.html', {
            'form': form,
            'incomes_by_category': incomes_by_category,
            'expenses_by_category': expenses_by_category
        })
    else:
        # Если форма не валидна, показываем только форму
        return render(request, 'budget/analysis.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('home')