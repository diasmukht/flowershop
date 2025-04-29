from django.db import models

class Bouquet(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='bouquets/')
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name



from django.db import models
from django.contrib.auth.models import User
from flowers.models import Bouquet
from constructor.models import CustomBouquet

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bouquet = models.ForeignKey(Bouquet, null=True, blank=True, on_delete=models.CASCADE)
    custom_bouquet = models.ForeignKey(CustomBouquet, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_price(self):
        if self.bouquet:
            return self.bouquet.price * self.quantity
        elif self.custom_bouquet:
            return self.custom_bouquet.total_price
        return 0
