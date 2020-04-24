from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, Client
from .forms import ClientForm, TransactionForm

def home(request):
    oldest_transactions = Transaction.objects.order_by('-created_at')[:5]
    return render(request, 'transactions/home.html', { 'transactions': oldest_transactions })

@login_required
def clients(request):
    clients = Client.objects.all()   
    return render(request, 'transactions/clients.html', { 'clients': clients, 'clients_page': 'active' })

@login_required
def new_client(request):
    if request.method == 'POST':
        try:
            form = ClientForm(request.POST)
            form.save()
            return redirect('transactions:clientes')
        except ValueError:
            return render(request, 'transactions/new_update_client.html', { 'form': form })
    else:
        client_form = ClientForm()
        return render(request, 'transactions/new_update_client.html', { 'form': client_form })

@login_required
def update_client(request, client_id):
    client = get_object_or_404(Client,pk=client_id)
    if request.method == 'POST':
        try:
            form = ClientForm(request.POST, instance=client)
            form.save()
            return redirect('transactions:clientes')
        except ValueError:
            return render(request, 'transactions/new_update_client.html', { 'form': form })
    else:
        client_form = ClientForm(instance=client)
        return render(request, 'transactions/new_update_client.html', { 'form': client_form, 'client': client })

@login_required
def view_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    return render(request, 'transactions/view_client.html', { 'client': client })

@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('transactions:clientes')

@login_required
def transactions(request):
    transactions = Transaction.objects.all()[:5]
    return render(request, 'transactions/transactions.html', { 'transactions': transactions, 'transactions_page': 'active'})

@login_required
def view_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    return render(request, 'transactions/view_transaction.html', { 'transaction': transaction })

@login_required
def new_transaction(request):
    if request.method == 'POST':
        try:
            form = TransactionForm(request.POST)
            newtransaction = form.save(commit=False)
            newtransaction.responsible = request.user
            newtransaction.save()
            return redirect('transactions:vales')
        except ValueError:
            return render(request, 'transactions/new_update_transaction.html', {'form': form })
    else:
        form = TransactionForm()
        return render(request, 'transactions/new_update_transaction.html', {'form': form })

@login_required
def update_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction,pk=transaction_id)
    if request.method == 'POST':
        try:
            form = TransactionForm(instance=transaction)
            form.save()        
            return redirect('transactions:vales')
        except ValueError:
            return render(request, 'transactions/new_update_transaction.html', {'form': form })
    else:
        form = TransactionForm(instance=transaction)
        return render(request, 'transactions/new_update_transaction.html', { 'form': form })

@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transactions:vales')
