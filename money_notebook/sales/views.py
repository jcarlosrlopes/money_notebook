from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.forms.models import inlineformset_factory
from django.utils.decorators import method_decorator
from .models import OnCreditSale, Client, Account, SaleItem
from .forms import ClientForm, OnCreditSaleForm, AccountForm, SaleItemForm
from django.urls import reverse_lazy

@method_decorator(login_required, 'dispatch')
class HomeListView(ListView):    
    template_name = 'sales/home.html'
    queryset = Account.objects.order_by('-created_at')[:5]
    context_object_name = 'oldest_accounts'
    # oldest_accounts = Account.objects.order_by('-created_at')[:5]
    # return render(request, 'sales/home.html', { 'accounts': oldest_accounts })

@method_decorator(login_required, 'dispatch')
class ClientsListView(ListView):
    template_name = 'sales/clients.html'
    context_object_name = 'clients'
    model = Client

@login_required
def new_client(request):
    if request.method == 'POST':
        try:
            form = ClientForm(request.POST)
            form.save()
            return redirect('sales:clientes')
        except ValueError:
            return render(request, 'sales/new_update_client.html', { 'form': form })
    else:
        client_form = ClientForm()
        return render(request, 'sales/new_update_client.html', { 'form': client_form })

@method_decorator(login_required, 'dispatch')
class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'sales/new_update_client.html'
    context_object_name = 'client'
    pk_url_kwarg = 'client_id'
    success_url = reverse_lazy('sales:clientes')
    
    # client = get_object_or_404(Client,pk=client_id)
    # if request.method == 'POST':
    #     try:
    #         form = ClientForm(request.POST, instance=client)
    #         form.save()
    #         return redirect('sales:clientes')
    #     except ValueError:
    #         return render(request, 'sales/new_update_client.html', { 'form': form })
    # else:
    #     client_form = ClientForm(instance=client)
    #     return render(request, 'sales/new_update_client.html', { 'form': client_form, 'client': client })

@method_decorator(login_required, 'dispatch')
class ClientDetailView(DetailView):
    model = Client
    template_name = 'sales/view_client.html'
    context_object_name = 'client'
    pk_url_kwarg = 'client_id'

@login_required
def delete_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        client.delete()
        return redirect('sales:clientes')

@method_decorator(login_required, 'dispatch')
class AccountsListView(ListView):
    template_name = 'sales/accounts.html'    
    context_object_name = 'accounts'
    model = Account

@method_decorator(login_required, 'dispatch')
class AccountDetailView(DetailView):
    model = Account
    template_name = 'sales/view_account.html'
    context_object_name = 'account'
    pk_url_kwarg = 'account_id'

@login_required
def new_account(request):
    if request.method == 'POST':
        try:
            form = AccountForm(request.POST)
            newaccount = form.save(commit=False)
            newaccount.created_by = request.user
            newaccount.save()
            return redirect('sales:accounts')
        except ValueError:
            return render(request, 'sales/new_update_account.html', {'form': form })
    else:
        form = AccountForm()
        return render(request, 'sales/new_update_account.html', {'form': form })

@method_decorator(login_required, 'dispatch')
class AccountUpdateView(UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'sales/new_update_account.html'
    context_object_name = 'account'
    pk_url_kwarg = 'account_id'
    success_url = reverse_lazy('sales:accounts')

# def update_account(request, account_id):
#     account = get_object_or_404(Account,pk=account_id)
#     if request.method == 'POST':
#         try:
#             form = AccountForm(instance=account)
#             form.save()        
#             return redirect('sales:accounts')
#         except ValueError:
#             return render(request, 'sales/new_update_account.html', {'form': form })
#     else:
#         form = AccountForm(instance=account)
#         return render(request, 'sales/new_update_account.html', { 'form': form })

@login_required
def delete_account(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    if request.method == 'POST':
        account.delete()
        return redirect('sales:accounts')

@login_required
def new_update_sale(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    SaleItemFormSet = inlineformset_factory(OnCreditSale, SaleItem, form=SaleItemForm, can_delete=False)
    if request.method == 'POST':
        try:            
            form = OnCreditSaleForm(request.POST, prefix='sale')
            sale = form.save(commit=False)
            sale.total_value = 0
            sale.account = account
            sale.created_by = request.user
            sale.save()

            formset = SaleItemFormSet(request.POST, prefix='items', instance=sale)
            if formset.is_valid():
                # for item_form in formset:
                #     item = item_form.save(commit=False)
                #     item.total_value = item.quantity * item.unit_price
                #     item.save()
                formset.save()

            # print(request.POST)

            return redirect(reverse('sales:view_account', kwargs={ 'account_id': account_id }))
        except ValueError:
            return render(request, 'sales/new_update_sale.html', { 'form': form })
    else:
        form = OnCreditSaleForm(prefix='sale')
        # SaleItemFormSet = inlineformset_factory(OnCreditSale, SaleItem, form=SaleItemForm, can_delete=False)
        formset = SaleItemFormSet(queryset=SaleItem.objects.none())
        # form = OnCreditSaleForm()
        return render(request, 'sales/new_update_sale.html', { 'sale_form': form, 'formset': formset })

def view_sale(request, account_id, sale_id):
    sale = OnCreditSale.objects.get(pk=sale_id)
    return render(request, 'sales/view_sale.html', { 'sale': sale })