from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'transactions'
urlpatterns = [
    path("", views.home, name="home"),    
    path("clients/", views.clients, name="clientes"),
    path("clients/new_client", views.new_client, name="new_client"),
    path("clients/<int:client_id>/update_client", views.update_client, name="update_client"),
    path("clients/<int:client_id>/", views.view_client, name="view_client"),
    path("clients/<int:client_id>/delete_client", views.delete_client, name="delete_client"),
    path("transactions/", views.transactions, name="vales"),
    path("transactions/new_transaction", views.new_transaction, name="new_transaction"),
    path("transactions/<int:transaction_id>/update_transaction", views.update_transaction, name="update_transaction"),
    path("transactions/<int:transaction_id>/", views.view_transaction, name="view_transaction"),
    path("transactions/<int:transaction_id>/delete_transaction", views.delete_transaction, name="delete_transaction"),
]
