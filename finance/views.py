from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Transaction

# Create your views here.
@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    income = sum(t.amount for t in transactions if t.type == 'Income')
    expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = income - expense

    context = {
        'transactions' : transactions,
        'income' : income,
        'expense' : expense,
        'balance' : balance,
    }

    return render(request, 'finance/dashboard.html', context)