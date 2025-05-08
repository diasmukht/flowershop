from django.db import models
from flowers.models import Flower

class CustomBouquet(models.Model):
    session_key = models.CharField(max_length=100, null=True, blank=True)
    flowers = models.ManyToManyField(Flower, through='CustomBouquetFlower')
    greenery = models.ManyToManyField('Greenery', through='CustomBouquetGreenery')
    packaging = models.ManyToManyField('Packaging', through='CustomBouquetPackaging')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    generated_image = models.ImageField(upload_to='generated_bouquets/', null=True, blank=True)

    def update_total_price(self):
        flower_total = sum(item.flower.price * item.quantity for item in self.custombouquetflower_set.all())
        greenery_total = sum(item.greenery.price * item.quantity for item in self.custombouquetgreenery_set.all())
        packaging_total = sum(item.packaging.price * item.quantity for item in self.custombouquetpackaging_set.all())
        self.total_price = flower_total + greenery_total + packaging_total
        self.save()
        self.update_generated_image()

    def update_generated_image(self):
        flower_items = self.custombouquetflower_set.select_related('flower').all()
        packaging_items = self.custombouquetpackaging_set.select_related('packaging').all()

        if not flower_items or not packaging_items:
            self.generated_image = None
            self.save()
            return

        flower_names = [item.flower.name.lower() for item in flower_items]
        packaging_name = packaging_items.first().packaging.name.lower()
        total_quantity = sum(item.quantity for item in flower_items)

        # Имя первого цветка в списке (основной для генерации по комбинации)
        main_flower = flower_items[0].flower.name.lower()

        if 15 <= total_quantity <= 51:

            if sorted(flower_names) == sorted(['роза', 'тюльпан', 'пион']):
                if total_quantity <= 24:
                    self.generated_image = f"generated_bouquets/special_3roses_15_{packaging_name}.png"
                elif total_quantity <= 39:
                    self.generated_image = f"generated_bouquets/special_3roses_30_{packaging_name}.png"
                else:
                    self.generated_image = f"generated_bouquets/special_3roses_50_{packaging_name}.png"

            elif sorted(flower_names) == sorted(['роза', 'тюльпан']):
                if total_quantity <= 24:
                    self.generated_image = f"generated_bouquets/special_3roses_15_{packaging_name}.png"
                elif total_quantity <= 39:
                    self.generated_image = f"generated_bouquets/special_3roses_30_{packaging_name}.png"
                else:
                    self.generated_image = f"generated_bouquets/special_3roses_50_{packaging_name}.png"

            elif len(flower_names) == 5:
                if total_quantity <= 24:
                    self.generated_image = f"generated_bouquets/combo5_{main_flower}_15_{packaging_name}.png"
                elif total_quantity <= 39:
                    self.generated_image = f"generated_bouquets/combo5_{main_flower}_30_{packaging_name}.png"
                else:
                    self.generated_image = f"generated_bouquets/combo5_{main_flower}_50_{packaging_name}.png"

            elif len(flower_names) == 4:
                if total_quantity <= 24:
                    self.generated_image = f"generated_bouquets/combo5_{main_flower}_15_{packaging_name}.png"
                elif total_quantity <= 39:
                    self.generated_image = f"generated_bouquets/combo5_{main_flower}_30_{packaging_name}.png"
                else:
                    self.generated_image = f"generated_bouquets/combo5_{main_flower}_50_{packaging_name}.png"

            elif len(flower_names) == 3:
                if total_quantity <= 24:
                    self.generated_image = f"generated_bouquets/combo3_{main_flower}_15_{packaging_name}.png"
                elif total_quantity <= 39:
                    self.generated_image = f"generated_bouquets/combo3_{main_flower}_30_{packaging_name}.png"
                else:
                    self.generated_image = f"generated_bouquets/combo3_{main_flower}_50_{packaging_name}.png"

            elif len(flower_names) == 2:
                if total_quantity <= 24:
                    self.generated_image = f"generated_bouquets/combo2_{main_flower}_15_{packaging_name}.png"
                elif total_quantity <= 39:
                    self.generated_image = f"generated_bouquets/combo2_{main_flower}_30_{packaging_name}.png"
                else:
                    self.generated_image = f"generated_bouquets/combo2_{main_flower}_50_{packaging_name}.png"

            elif len(flower_names) == 1:
                if total_quantity == 15:
                    self.generated_image = f"generated_bouquets/{main_flower}_15_{packaging_name}.png"
                elif total_quantity <= 20:
                    self.generated_image = f"generated_bouquets/{main_flower}_20_{packaging_name}.png"
                elif total_quantity <= 30:
                    self.generated_image = f"generated_bouquets/{main_flower}_30_{packaging_name}.png"
                elif total_quantity <= 40:
                    self.generated_image = f"generated_bouquets/{main_flower}_40_{packaging_name}.png"
                else:
                    self.generated_image = f"generated_bouquets/{main_flower}_50_{packaging_name}.png"
            else:
                self.generated_image = None
        else:
            self.generated_image = None

        self.save()

    def __str__(self):
        return f"Кастомный букет #{self.id}"


class CustomBouquetFlower(models.Model):
    custom_bouquet = models.ForeignKey(CustomBouquet, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.flower.name} x {self.quantity}"


class Greenery(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='greenery/')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Wrap(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='wraps/')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CustomBouquetGreenery(models.Model):
    custom_bouquet = models.ForeignKey(CustomBouquet, on_delete=models.CASCADE)
    greenery = models.ForeignKey(Greenery, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Packaging(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='packaging/')

    def __str__(self):
        return self.name


class CustomBouquetPackaging(models.Model):
    custom_bouquet = models.ForeignKey(CustomBouquet, on_delete=models.CASCADE)
    packaging = models.ForeignKey(Packaging, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
