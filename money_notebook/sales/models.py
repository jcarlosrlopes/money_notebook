from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Sum

# Create your models here.
class ClientAccount(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True)
    cpf = models.BigIntegerField(unique=True)
    phone = models.BigIntegerField(blank=True, null=True)
    limit = models.DecimalField(max_digits=6,decimal_places=2, default=0)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='accounts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class OnCreditSale(models.Model):
    account = models.ForeignKey(ClientAccount, on_delete=models.CASCADE, related_name='sales')
    description = models.CharField(max_length=100, blank=True)
    total_value = models.DecimalField(max_digits=6,decimal_places=2, default=0)
    receipt = models.ImageField(upload_to='sales/images', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

    def calculate_total(self):
        items_total = SaleItem.objects.filter(sale_id=self.id).aggregate(
                        total=Sum(F('unit_price') * F('quantity'),
                        output_field=models.DecimalField(decimal_places=2))
                      )
        payments_total = Payment.objects.filter(sale_id=self.id).aggregate(
                            total=Sum(F('value'),
                            output_field=models.DecimalField(decimal_places=2))
                        )
        self.total_value = items_total['total'] - payments_total['total']

class SaleItem(models.Model):
    sale = models.ForeignKey(OnCreditSale, on_delete=models.CASCADE, related_name='items')
    quantity = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    description = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.description    

class Payment(models.Model):
    description = models.CharField(max_length=100, blank=True)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField()
    sale = models.ForeignKey(OnCreditSale, on_delete=models.CASCADE, related_name='payments')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.description