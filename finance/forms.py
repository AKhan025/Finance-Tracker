from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        field = ['type', 'amount', 'category', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type' : 'date'}),
            'description' : forms.Textarea(attrs={'rows' : 2}),
        }

