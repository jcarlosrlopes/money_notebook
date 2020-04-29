from django import forms
from .models import Client, Account, OnCreditSale, SaleItem, Payment as SalePayment


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'address', 'cpf', 'phone']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['client']

class OnCreditSaleForm(forms.ModelForm):
    class Meta:
        model = OnCreditSale
        fields = ['description','receipt']        

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['sale', 'quantity', 'description', 'unit_price', 'total_value']

class Payment(forms.ModelForm):
    class Meta:
        model = SalePayment
        fields = ['value', 'date', 'sale']