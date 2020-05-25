from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.forms.models import inlineformset_factory
from django.forms.formsets import all_valid
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Sum
from .models import OnCreditSale, ClientAccount, SaleItem
from .forms import ClientAccountForm, OnCreditSaleForm, SaleItemForm
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory

class SaleItemInline(InlineFormSetFactory):
    model = SaleItem
    form_class = SaleItemForm

@method_decorator(login_required, 'dispatch')
class HomeListView(ListView):
    model = OnCreditSale
    template_name = 'sales/home.html'
    queryset = OnCreditSale.objects.order_by('created_at')[:5]
    context_object_name = 'oldest_sales'
    paginate_by = 10

# @method_decorator(login_required, 'dispatch')
# class ClientsListView(ListView):
#     template_name = 'sales/clients.html'
#     context_object_name = 'clients'
#     model = ClientAccount
#     paginate_by = 10

# @login_required
# def new_client(request):
#     if request.method == 'POST':
#         try:
#             form = ClientAccountForm(request.POST)
#             form.save()
#             return redirect('sales:clientes')
#         except ValueError:
#             return render(request, 'sales/new_update_client.html', { 'form': form })
#     else:
#         client_form = ClientAccountForm()
#         return render(request, 'sales/new_update_client.html', { 'form': client_form })

# @method_decorator(login_required, 'dispatch')
# class ClientUpdateView(UpdateView):
#     model = ClientAccount
#     form_class = ClientAccountForm
#     template_name = 'sales/new_update_client.html'
#     context_object_name = 'client'
#     pk_url_kwarg = 'client_id'
#     success_url = reverse_lazy('sales:clientes')

# @method_decorator(login_required, 'dispatch')
# class ClientDetailView(DetailView):
#     model = ClientAccount
#     template_name = 'sales/view_client.html'
#     context_object_name = 'client'
#     pk_url_kwarg = 'client_id'

# @login_required
# def delete_client(request, client_id):
#     client = get_object_or_404(ClientAccount, pk=client_id)
#     if request.method == 'POST':
#         client.delete()
#         return redirect('sales:clientes')

@method_decorator(login_required, 'dispatch')
class AccountsListView(ListView):
    template_name = 'sales/accounts.html'    
    context_object_name = 'accounts'
    model = ClientAccount
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["accounts_page"] = 'active'
        return context    

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.annotate(total_value=Sum('sales__total_value')).order_by('created_at')
    

@method_decorator(login_required, 'dispatch')
class AccountDetailView(DetailView):
    model = ClientAccount
    template_name = 'sales/view_account.html'
    context_object_name = 'account'
    pk_url_kwarg = 'account_id'

@method_decorator(login_required, 'dispatch')
class AccountCreateView(CreateView):
    model = ClientAccount
    template_name = 'sales/new_update_account.html'
    form_class = ClientAccountForm    

    def form_valid(self, form):
        newaccount = form.save(commit=False)
        newaccount.created_by = self.request.user
        newaccount.save()
        return redirect('sales:accounts')
    
# def new_account(request):
#     if request.method == 'POST':
#         try:
#             form = ClientAccountForm(request.POST)
#             newaccount = form.save(commit=False)
#             newaccount.created_by = request.user
#             newaccount.save()
#             return redirect('sales:accounts')
#         except ValueError:
#             return render(request, 'sales/new_update_account.html', {'form': form })
#     else:
#         form = ClientAccountForm()
        # return render(request, 'sales/new_update_account.html', {'form': form })

@method_decorator(login_required, 'dispatch')
class AccountUpdateView(UpdateView):
    model = ClientAccount
    form_class = ClientAccountForm
    template_name = 'sales/new_update_account.html'
    context_object_name = 'account'
    pk_url_kwarg = 'account_id'
    success_url = reverse_lazy('sales:accounts')

@method_decorator(login_required, 'dispatch')
class AccountDeleteView(SuccessMessageMixin, DeleteView):
    model = ClientAccount
    template_name = 'sales/delete_account.html'
    context_object_name = 'account'
    success_url = reverse_lazy('sales:accounts')
    pk_url_kwarg = 'account_id'
    success_message = "Conta excluída com sucesso!"

# @login_required
# def new_update_sale(request, account_id):
#     account = get_object_or_404(ClientAccount, pk=account_id)
#     SaleItemFormSet = inlineformset_factory(OnCreditSale, SaleItem, form=SaleItemForm, can_delete=False)
#     if request.method == 'POST':
#         try:
#             with transaction.atomic():
#                 form = OnCreditSaleForm(request.POST, prefix='sale')
#                 sale = form.save(commit=False)
#                 sale.total_value = 0
#                 sale.account = account
#                 sale.created_by = request.user
#                 sale.save()

#                 formset = SaleItemFormSet(request.POST, prefix='items', instance=sale)
#                 sale_total = 0
#                 if formset.is_valid():
#                     items_form = formset.save(commit=False)
#                     print(items_form)
#                     for item in items_form:
#                         item.total_value = item.quantity * item.unit_price
#                         sale_total += item.total_value
#                         item.save()

#                     sale_update = OnCreditSale.objects.select_for_update().get(pk=sale.id)
#                     sale_update.total_value = sale_total
#                     sale_update.save()

#             return redirect(reverse('sales:view_account', kwargs={ 'account_id': account_id }))
#         except ValueError:
#             return render(request, 'sales/new_update_sale.html', { 'form': form })
#     else:
#         form = OnCreditSaleForm(prefix='sale')
#         formset = SaleItemFormSet(queryset=SaleItem.objects.none())
#         return render(request, 'sales/new_update_sale.html', { 'sale_form': form, 'item_formset': formset })

@method_decorator(login_required, 'dispatch')
class SaleCreateView(CreateWithInlinesView):
    model = OnCreditSale
    inlines = [SaleItemInline]
    fields = ['description', 'receipt']
    template_name = 'sales/new_update_sale.html'

@method_decorator(login_required, 'dispatch')
class SalesListView(ListView):
    model = OnCreditSale
    template_name = 'sales/sales.html'
    context_object_name = 'sales'    
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sales_page"] = 'active'
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('created_at')

@method_decorator(login_required, 'dispatch')
class SaleDetailView(DetailView):
    model = OnCreditSale
    template_name = 'sales/view_sale.html'
    context_object_name = 'sale'
    pk_url_kwarg = 'sale_id'

@method_decorator(login_required, 'dispatch')
class SaleDeleteView(DeleteView):
    model = OnCreditSale
    template_name = 'sales/delete_sale.html'
    pk_url_kwarg = 'sale_id'
    success_url = reverse_lazy('sales:sales')
    context_object_name = 'sale'

@method_decorator(login_required, 'dispatch')
class SaleUpdateView(UpdateWithInlinesView):
    model = OnCreditSale    
    inlines = [SaleItemInline]
    template_name = 'sales/new_update_sale.html'
    pk_url_kwarg = 'sale_id'
    fields = ['description', 'receipt']
    success_url = reverse_lazy('sales:sales')


    # model = OnCreditSale
    # form_class = OnCreditSaleForm

    # def get(self, request, *args, **kwargs):
    #     """
    #     Handles GET requests and instantiates a blank version of the form and formsets.
    #     """
    #     self.object = self.get_object()
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     SaleItemFormSet = inlineformset_factory(OnCreditSale, SaleItem, form=SaleItemForm, can_delete=False, extra=1)
    #     inlines = SaleItemFormSet(instance=self.object)
    #     return self.render_to_response(
    #         self.get_context_data(form=form, inlines=inlines, **kwargs)
    #     )

    # def post(self, request, *args, **kwargs):
    #     """
    #     Handles POST requests, instantiating a form and formset instances with the
    #     passed POST variables and then checked for validity.
    #     """
    #     self.object = self.get_object()
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)

    #     initial_object = self.object
    #     if form.is_valid():
    #         self.object = form.save(commit=False)
    #         form_validated = True
    #     else:
    #         form_validated = False

    #     SaleItemFormSet = inlineformset_factory(OnCreditSale, SaleItem, form=SaleItemForm, can_delete=False, extra=1)
    #     inlines = SaleItemFormSet()        

    #     if all_valid(inlines) and form_validated:
    #         return self.forms_valid(form, inlines)
    #     self.object = initial_object
    #     return self.forms_invalid(form, inlines)

    # def forms_valid(self, form, inlines):
    #     """
    #     If the form and formsets are valid, save the associated models.
    #     """
    #     response = self.form_valid(form)
    #     for formset in inlines:
    #         formset.save()
    #     return response

    # def forms_invalid(self, form, inlines):
    #     """
    #     If the form or formsets are invalid, re-render the context data with the
    #     data-filled form and formsets and errors.
    #     """
    #     return self.render_to_response(
    #         self.get_context_data(form=form, inlines=inlines)
    #     )

    # def get_context_data(self, **kwargs):
    #     context = super(SaleUpdateView, self).get_context_data(**kwargs)
    #     SaleItemFormSet = inlineformset_factory(OnCreditSale, SaleItem, form=SaleItemForm, can_delete=False, extra=1)
    #     # context["formset"] = SaleItemFormSet(instance=self.object)        
    #     if self.request.POST:            
    #         context['sale_form'] = OnCreditSaleForm(self.request.POST, instance=self.object)
    #         context['item_formset'] = SaleItemFormSet(self.request.POST, instance=self.object)
    #     else:            
    #         context['sale_form'] = OnCreditSaleForm(instance=self.object)
    #         context['item_formset'] = SaleItemFormSet(instance=self.object)
    #     return context

    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     print(form)
    #     print(self.get_object())
    #     print(context["sale_form"])        
        
    #     # sale_update = OnCreditSale.objects.select_for_update().get(pk=self.object.id)
    #     item_form = context['item_formset']
    #     if item_form.is_valid():
    #         self.object = form.save()
    #         item_form.instance = self.object
    #         item_form.save()

    #     # print(self.object)

    #     return redirect(reverse('sales:view_sale', kwargs={ 'account_id': self.object.account.id, 'sale_id': self.object.id }))        
        
    # form = OnCreditSaleForm(prefix='sale')
    # # SaleItemFormSet = inlineformset_factory(OnCreditSale, SaleItem, form=SaleItemForm, can_delete=False)
    # formset = SaleItemFormSet(queryset=SaleItem.objects.none())

@login_required
def delete_sale(request, sale_id):
    sale = get_object_or_404(OnCreditSale, pk=sale_id)
    if request.method == 'POST':
        sale.delete()
        return redirect('sales:sales')

# def view_sale(request, account_id, sale_id):
#     sale = OnCreditSale.objects.get(pk=sale_id)
#     return render(request, 'sales/view_sale.html', { 'sale': sale })