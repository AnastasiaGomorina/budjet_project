from django import forms
from .models import IncomeCategory, ExpenseCategory, Income, Expense

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['category', 'amount', 'date']

        category = forms.ModelChoiceField(queryset=IncomeCategory.objects.all(), empty_label="Select a Category")

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date']

        category = forms.ModelChoiceField(queryset=ExpenseCategory.objects.all(), empty_label="Select a Category")

class PeriodForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Choose", "Choose", "Choose")))
    end_date = forms.DateField(widget=forms.SelectDateWidget(empty_label=("Choose", "Choose", "Choose")))