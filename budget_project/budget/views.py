from django.shortcuts import render, redirect
from .forms import IncomeForm, ExpenseForm

def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'budget/add_income.html', {'form': form})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'budget/add_expense.html', {'form': form})

def home(request):
    return render(request, 'budget/base.html')

def income_list(request):
    return render(request, 'budget/income_list.html')

def expense_list(request):
    return render(request, 'budget/expense_list.html')

def analysis_view(request):
    return render(request, 'budget/analysis.html')