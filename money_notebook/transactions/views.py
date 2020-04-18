from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from .models import Transaction, Client

# Create your views here.
def home(request):
    oldest_transactions = Transaction.objects.order_by('-created_at')[:5]
    return render(request, 'transactions/home.html', { 'transactions': oldest_transactions })

def clients(request):
    clients = Client.objects.all()[:5]
    return render(request, 'transactions/clients.html', { 'clients': clients })

def new_client(request):
    return render(request, 'transactions/new_update_client.html', {})

def view_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    return render(request, 'transactions/view_client.html', { 'client': client })

def delete_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('clients')

def transactions(request):
    return render(request, 'transactions/transactions.html', {})

def new_transaction(request):
    return render(request, 'transactions/new_transaction.html', {})

def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transactions')
