from django import forms
from .models import Client, Transaction

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'address', 'cpf', 'phone']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['value', 'transaction_type', 'client', 'description']