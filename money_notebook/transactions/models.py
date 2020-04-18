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

class Transaction(models.Model):
    TRANSACTION_CHOICES = [
        ('PA','Pagamento'),
        ('DE','Despesa'),
    ]

    value = models.DecimalField(max_digits=5,decimal_places=2,)
    transaction_type = models.CharField(max_length=2,choices=TRANSACTION_CHOICES)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='transactions')
    description = models.TextField(blank=True)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description