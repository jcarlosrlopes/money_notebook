from django.urls import path
from . import views

app_name = 'transactions'
urlpatterns = [
    path("", views.home, name="home"),
    path("clients/", views.clients, name="clientes"),
    path("clients/new_client", views.new_client, name="new_client"),
    path("clients/<int:client_id>/view_client", views.view_client, name="view_client"),
    path("clients/<int:client_id>/delete_client", views.delete_client, name="delete_client"),
    path("transactions/", views.transactions, name="vales"),
    path("transactions/new_transaction", views.new_transaction, name="new_transaction"),
    path("transactions/delete_transaction", views.delete_transaction, name="delete_transaction"),
]
