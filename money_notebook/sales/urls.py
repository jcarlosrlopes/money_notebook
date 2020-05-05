from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import *

app_name = 'sales'
urlpatterns = [
    path("", HomeListView.as_view(), name="home"),    
    path("clientes/", ClientsListView.as_view(), name="clientes"),
    path("clientes/novo", views.new_client, name="new_client"),
    path("clientes/<int:client_id>/", ClientDetailView.as_view(), name="view_client"),
    path("clientes/<int:client_id>/atualizar", ClientUpdateView.as_view(), name="update_client"),
    path("clientes/<int:client_id>/excluir", views.delete_client, name="delete_client"),
    path("contas/", AccountsListView.as_view(), name="accounts"),
    path("contas/nova", views.new_account, name="new_account"),
    path("contas/<int:account_id>/", AccountDetailView.as_view(), name="view_account"),
    path("contas/<int:account_id>/atualizar", AccountUpdateView.as_view(), name="update_account"),
    path("contas/<int:account_id>/excluir", views.delete_account, name="delete_account"),
    path("contas/<int:account_id>/novo_vale", views.new_update_sale, name="new_update_sale"),
    path("contas/<int:account_id>/vales/<int:sale_id>", views.view_sale, name="view_sale")
]
