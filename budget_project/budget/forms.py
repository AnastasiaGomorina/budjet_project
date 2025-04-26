from django import forms
from .models import Income, Expense

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['user', 'category', 'amount', 'date']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['user', 'category', 'amount', 'date']
