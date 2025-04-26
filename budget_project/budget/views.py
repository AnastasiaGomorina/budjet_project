from django.shortcuts import render

def home(request):
    return render(request, 'budget/base.html')

def income_list(request):
    return render(request, 'budget/income_list.html')

def expense_list(request):
    return render(request, 'budget/expense_list.html')

def analysis_view(request):
    return render(request, 'budget/analysis.html')