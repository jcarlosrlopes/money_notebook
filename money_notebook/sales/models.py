from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200,blank=True)
    cpf = models.CharField(max_length=11,unique=True)
    phone = models.CharField(max_length=11,blank=True)

    def __str__(self):
        return self.name

class Account(models.Model):
    current_value = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='accounts')
    created_at = models.DateTimeField(auto_now_add=True)

class OnCreditSale(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sales')
    description = models.CharField(max_length=100, blank=True)
    total_value = models.DecimalField(max_digits=6,decimal_places=2,)
    receipt = models.ImageField(upload_to='sales/images', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

class SaleItem(models.Model):
    sale = models.ForeignKey(OnCreditSale, on_delete=models.CASCADE, related_name='items')
    quantity = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    description = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    total_value = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return self.description

class Payment(models.Model):
    value = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField()
    sale = models.ForeignKey(OnCreditSale, on_delete=models.CASCADE, related_name='payments')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.value