from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm

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


@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid:
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()

    return render(request, 'finance/add_transaction.html', {'form' : form})