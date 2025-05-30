from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import IncomeForm, ExpenseForm, PeriodForm
from django.db.models import Sum
from .models import Income, Expense, IncomeCategory, ExpenseCategory
from django.contrib.auth.decorators import login_required
from datetime import date
import calendar


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'budget/register.html', {'form': form})


@login_required
def incomes_view(request):
    today = date.today()
    default_start_date = date(today.year, today.month, 1)
    last_day = calendar.monthrange(today.year, today.month)[1]
    default_end_date = date(today.year, today.month, last_day)

    if request.GET:
        form = PeriodForm(request.GET)
    else:
        form = PeriodForm(initial={
            'start_date': default_start_date,
            'end_date': default_end_date
        })

    if form.is_valid():
        # Если пользователь ввел период
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
    else:
        # Иначе — текущий месяц
        start_date = default_start_date
        end_date = default_end_date

    incomes = Income.objects.filter(user=request.user, date__range=[start_date, end_date]).order_by('date')

    total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0

    no_incomes = incomes.count() == 0

    return render(request, 'budget/income_list.html', {'form': form, 'incomes': incomes, 'total_income': total_income, 'no_incomes': no_incomes})


@login_required
def expense_list(request):
    today = date.today()
    default_start_date = date(today.year, today.month, 1)
    last_day = calendar.monthrange(today.year, today.month)[1]
    default_end_date = date(today.year, today.month, last_day)

    if request.GET:
        form = PeriodForm(request.GET)
    else:
        form = PeriodForm(initial={
            'start_date': default_start_date,
            'end_date': default_end_date
        })

    if form.is_valid():
        # Если пользователь ввел период
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
    else:
        # Иначе — текущий месяц
        start_date = default_start_date
        end_date = default_end_date

    expenses = Expense.objects.filter(user=request.user, date__range=[start_date, end_date]).order_by('date')

    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0

    no_expenses = expenses.count() == 0

    return render(request, 'budget/expense_list.html', {'form': form, 'expenses': expenses, 'total_expense': total_expense, 'no_expenses': no_expenses})


@login_required
def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    income.delete()
    return redirect('income_list')


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    expense.delete()
    return redirect('expense_list')


@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'budget/add_income.html', {'form': form, 'income': None})


@login_required
def edit_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'budget/add_income.html', {'form': form, 'income': income})


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
    return render(request, 'budget/add_expense.html', {'form': form, 'expense': None})


@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'budget/add_expense.html', {'form': form, 'expense': expense})


MONTHS_RU = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}



def home(request):
    if request.user.is_authenticated:
        total_income_all = Income.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
        total_expense_all = Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
        balance = total_income_all - total_expense_all

        today = date.today()
        start_date = date(today.year, today.month, 1)
        last_day = calendar.monthrange(today.year, today.month)[1]
        end_date = date(today.year, today.month, last_day)

        total_income_month = Income.objects.filter(
            user=request.user,
            date__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_expense_month = Expense.objects.filter(
            user=request.user,
            date__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))['total'] or 0

        current_month_ru = f"{MONTHS_RU[today.month]} {today.year}"

        return render(request, 'budget/base.html', {
            'balance': balance,
            'total_income_month': total_income_month,
            'total_expense_month': total_expense_month,
            'current_month': current_month_ru,
        })
    return render(request, 'budget/base.html')


@login_required
def analysis_view(request):
    today = date.today()
    default_start_date = date(today.year, today.month, 1)
    last_day = calendar.monthrange(today.year, today.month)[1]
    default_end_date = date(today.year, today.month, last_day)

    if request.GET:
        form = PeriodForm(request.GET)
    else:
        form = PeriodForm(initial={
            'start_date': default_start_date,
            'end_date': default_end_date
        })

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
    else:
        start_date = default_start_date
        end_date = default_end_date

    incomes = Income.objects.filter(user=request.user, date__range=[start_date, end_date])
    expenses = Expense.objects.filter(user=request.user, date__range=[start_date, end_date])

    no_incomes = incomes.count() == 0
    no_expenses = expenses.count() == 0

    incomes_by_category = incomes.values('category__name').annotate(total=Sum('amount'))
    expenses_by_category = expenses.values('category__name').annotate(total=Sum('amount'))

    def custom_sort(queryset):
        sorted_queryset = sorted(queryset, key=lambda x: x['category__name'])
        for i, item in enumerate(sorted_queryset):
            if item['category__name'] == 'Другое':
                sorted_queryset.append(sorted_queryset.pop(i))
                break
        return sorted_queryset

    incomes_by_category = custom_sort(incomes_by_category)
    expenses_by_category = custom_sort(expenses_by_category)

    return render(request, 'budget/analysis.html', {
        'form': form,
        'incomes_by_category': incomes_by_category,
        'expenses_by_category': expenses_by_category,
        'no_incomes': no_incomes,
        'no_expenses': no_expenses
    })


def logout_view(request):
    logout(request)
    return redirect('home')
