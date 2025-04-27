from django import forms
from .models import IncomeCategory, ExpenseCategory, Income, Expense

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['user', 'category', 'amount', 'date']

        category = forms.ModelChoiceField(queryset=IncomeCategory.objects.all(), empty_label="Select a Category")

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['user', 'category', 'amount', 'date']

        category = forms.ModelChoiceField(queryset=ExpenseCategory.objects.all(), empty_label="Select a Category")
