import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Transaction, Category
from .forms import TransactionForm

# Create your views here.
@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    income = sum(t.amount for t in transactions if t.type == 'Income')
    expense = sum(t.amount for t in transactions if t.type == 'Expense')
    balance = income - expense

    categories = Category.objects.all()
    category_name = [c.name for c in categories]
    category_totals = []

    for category in categories:
        total = Transaction.objects.filter(category=category).aggregate(Sum('amount'))['amount__sum'] or 0
        category_totals.append(total)

    income_total = Transaction.objects.filter(type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    expense_total = Transaction.objects.filter(type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'transactions' : transactions,
        'income' : income,
        'expense' : expense,
        'balance' : balance,
        'category_name': category_name,
        'category_totals': category_totals,
        'income_total': income_total,
        'expense_total': expense_total,
    }

    return render(request, 'finance/dashboard.html', context)


@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()

    return render(request, 'finance/add_transaction.html', {'form': form})

def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    form = TransactionForm(request.POST or None, instance=transaction)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'finance/edit_transaction.html', {'form': form})

def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        transaction.delete()
        return redirect('dashboard')
    return render(request, 'finance/delete_transaction.html', {'transaction': transaction})