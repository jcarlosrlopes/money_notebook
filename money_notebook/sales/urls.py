from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import *

app_name = 'sales'
urlpatterns = [
    path("", HomeListView.as_view(), name="home"),
    path("contas/", AccountsListView.as_view(), name="accounts"),
    path("contas/nova", AccountCreateView.as_view(), name="new_account"),
    path("contas/<int:account_id>/", AccountDetailView.as_view(), name="view_account"),
    path("contas/<int:account_id>/editar", AccountUpdateView.as_view(), name="update_account"),
    path("contas/<int:account_id>/excluir", AccountDeleteView.as_view(), name="delete_account"),
    path("contas/<int:account_id>/novo_vale", SaleCreateView.as_view(), name="new_account_sale"),
    path("contas/<int:account_id>/vales/<int:sale_id>", SaleDetailView.as_view(), name="view_sale"),
    path("vales/", SalesListView.as_view(), name="sales"),
    path("vales/novo", SaleCreateView.as_view(), name="new_sale"),
    path("vales/<int:sale_id>/excluir", SaleDeleteView.as_view(),name="delete_sale"),
    path("vales/<int:sale_id>/editar", SaleUpdateView.as_view(),name="update_sale"),
    path("vales/<int:sale_id>/items/novo", SaleItemCreateView.as_view(), name="new_item"),
    path("vales/<int:sale_id>/items/<int:item_id>/editar", SaleItemUpdateView.as_view(), name="update_item"),
    path("vales/<int:sale_id>/items/<int:item_id>/excluir", SaleItemDeleteView.as_view(), name="delete_item"),
    path("vales/<int:sale_id>/pagamentos/", PaymentListView.as_view(), name="payments"),
    path("vales/<int:sale_id>/pagamentos/novo", PaymentCreateView.as_view(), name="new_payment"),
    path("vales/<int:sale_id>/pagamentos/<int:payment_id>/editar", PaymentUpdateView.as_view(), name="update_payment"),
    path("vales/<int:sale_id>/pagamentos/<int:payment_id>/excluir", PaymentDeleteView.as_view(), name="delete_payment"),
]
