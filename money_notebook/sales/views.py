from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Sum
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from .models import OnCreditSale, ClientAccount, SaleItem, Payment
from .forms import ClientAccountForm, OnCreditSaleForm, SaleItemForm, PaymentForm

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

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.annotate(total_value=Sum('sales__total_value'))

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

@method_decorator(login_required, 'dispatch')
class SaleCreateView(CreateWithInlinesView):
    model = OnCreditSale
    inlines = [SaleItemInline]
    fields = ['description', 'receipt']
    template_name = 'sales/new_update_sale.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Check permissions for the request.user here
        if 'account_id' not in kwargs:
            self.fields = ['account', 'description', 'receipt']
        return super().dispatch(request, *args, **kwargs)

    def forms_valid(self, form, inlines):
        if 'account_id' in self.kwargs:
            form.instance.account = ClientAccount.objects.get(pk=self.kwargs['account_id'])
            
        form.instance.created_by = self.request.user

        with transaction.atomic():
            self.object = form.save()
            
            response = self.form_valid(form)
            items = inlines[0].save(commit=False)
            for item in items:            
                item.created_by = self.request.user                
                item.save()

            self.object.calculate_total()
            self.object.save()

        return redirect(self.object.get_absolute_url())
        
@method_decorator(login_required, 'dispatch')
class SaleUpdateView(UpdateWithInlinesView):
    model = OnCreditSale    
    inlines = [SaleItemInline]
    template_name = 'sales/new_update_sale.html'
    pk_url_kwarg = 'sale_id'
    fields = ['description', 'receipt']
    success_url = reverse_lazy('sales:sales')

    def forms_valid(self, form, inlines):
        with transaction.atomic():            
            response = self.form_valid(form)
            items = inlines[0].save(commit=False)
            for item in items:
                item.created_by = self.request.user                
                item.save()

            self.object.calculate_total()
            self.object.save()

        return redirect(self.object.get_absolute_url())

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.get_object().items.all()
        return context

@method_decorator(login_required, 'dispatch')
class SaleDeleteView(DeleteView):
    model = OnCreditSale
    template_name = 'sales/delete_sale.html'
    pk_url_kwarg = 'sale_id'
    # success_url = reverse_lazy('sales:sales')
    context_object_name = 'sale'

    def delete(self, request, *args, **kwargs):
        if 'account_id' in self.kwargs:
            self.success_url = redirect('sales:accounts', kwargs={ 'account_id': self.kwargs['account_id']})
        else:
            self.success_url = reverse_lazy('sales:sales')
            
        return super().delete(request, *args, **kwargs)

@method_decorator(login_required, 'dispatch')
class SaleItemCreateView(CreateView):
    model = SaleItem
    template_name = 'sales/new_update_item.html'
    form_class = SaleItemForm

    def form_valid(self, form):
        newsaleitem = form.save(commit=False)
        sale = OnCreditSale.objects.get(pk=self.kwargs['sale_id'])

        newsaleitem.sale = sale
        newsaleitem.save()

        sale.calculate_total()
        sale.save()

        return redirect(reverse('sales:view_sale',kwargs={ 'sale_id': sale.id }))

@method_decorator(login_required, 'dispatch')
class SaleItemUpdateView(UpdateView):
    model = SaleItem
    template_name = 'sales/new_update_item.html'
    form_class = SaleItemForm
    pk_url_kwarg = 'item_id'    

    def form_valid(self, form):
        with transaction.atomic():
            payment = form.save(commit=False)
            payment.save()
           
            # Update the sale total value
            sale = OnCreditSale.objects.select_for_update(pk=self.kwargs['sale_id'])
            sale.calculate_total()
            sale.save()

        return redirect(reverse('sales:view_sale',kwargs={ 'sale_id': sale.id }))

class SaleItemDeleteView(DeleteView):
    model = SaleItem
    template_name = 'sales/delete_item.html'
    context_object_name = 'item'
    success_url = reverse_lazy('sales:view_sale')
    pk_url_kwarg = 'item_id'

    def delete(self, request, *args, **kwargs):
        with transaction.atomic():
            super().delete(request, *args, **kwargs)

            # Update the sale total value
            sale = OnCreditSale.objects.select_for_update(pk=kwargs['sale_id'])
            sale.calculate_total()
            sale.save()

        return redirect(self.get_success_url(), kwargs= { 'sale_id': kwargs['sale_id']})
    
@method_decorator(login_required, 'dispatch')
class PaymentListView(ListView):
    model = Payment
    template_name = 'sales/payments.html'
    context_object_name = 'payments'
    paginate_by = 10

    def get_queryset(self):
        return Payment.objects.filter(sale_id=self.kwargs['sale_id']).order_by('date')    
    
@method_decorator(login_required, 'dispatch')
class PaymentCreateView(CreateView):
    model = Payment
    template_name = 'sales/new_update_payment.html'
    form_class = PaymentForm
    success_url = reverse_lazy('sales:payments')

    def form_valid(self, form):
        newpayment = form.save(commit=False)
        sale = OnCreditSale.objects.get(pk=self.kwargs['sale_id'])

        newpayment.sale = sale
        newpayment.created_by = self.request.user
        newpayment.save()

        sale.calculate_total()
        sale.save()

        return redirect(reverse('sales:payments',kwargs={ 'sale_id': sale.id }))

@method_decorator(login_required, 'dispatch')
class PaymentUpdateView(UpdateView):
    model = Payment
    template_name = 'sales/new_update_payment.html'
    form_class = PaymentForm
    pk_url_kwarg = 'payment_id'
    success_url = 'sales:payments'

    def form_valid(self, form):
        with transaction.atomic():
            payment = form.save(commit=False)
            payment.save()
           
            # Update the sale total value
            sale = OnCreditSale.objects.select_for_update().get(pk=self.kwargs['sale_id'])
            sale.calculate_total()
            sale.save()

        return redirect(reverse('sales:payments',kwargs={ 'sale_id': sale.id }))
    
@method_decorator(login_required, 'dispatch')
class PaymentDeleteView(DeleteView):
    model = Payment
    template_name = 'sales/delete_payment.html'
    context_object_name = 'payment'
    success_url = reverse_lazy('sales:sales')
    pk_url_kwarg = 'payment_id'

    def delete(self, request, *args, **kwargs):
        with transaction.atomic():
            super().delete(request, *args, **kwargs)

            # Update the sale total value
            sale = OnCreditSale.objects.select_for_update().get(pk=kwargs['sale_id'])
            sale.calculate_total()
            sale.save()

        return redirect(self.get_success_url())