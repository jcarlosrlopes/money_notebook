from sales.models import *
import random
import datetime

def create_accounts():
    user = User.objects.get(pk=1)
    for c in range(1,11):
        client = ClientAccount.objects.create(name=f'Client {c}',cpf=random.randint(11111111111,99999999999),created_by=user)
        for s in range(1,11):
            sale = OnCreditSale.objects.create(account=client, description=f'Sale {s} of {client.name}', created_by=user)
            for i in range(1,11):
                quantity = random.randint(1,11)
                price = random.random()*10
                SaleItem.objects.create(sale=sale, description=f'Item {i} of {sale.description}',quantity=quantity,unit_price=price,total_value=quantity*price)

                if i % 2 == 0:
                    Payment.objects.create(description=f'Payment {i} of {sale.description}', value=random.randint(1,11), date=datetime.datetime.now(),sale=sale, created_by=user)

if __name__ == "__main__":
    create_accounts()