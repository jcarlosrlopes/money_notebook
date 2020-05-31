from django import forms
from .models import ClientAccount, OnCreditSale, SaleItem, Payment as SalePayment


class ClientAccountForm(forms.ModelForm):
    class Meta:
        model = ClientAccount
        fields = ['name', 'address', 'cpf', 'phone', 'limit']

class OnCreditSaleForm(forms.ModelForm):
    class Meta:
        model = OnCreditSale
        fields = ['description','receipt']        

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['quantity', 'description', 'unit_price']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = SalePayment
        fields = ['description', 'value', 'date']