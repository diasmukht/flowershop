# flowers/models.py
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Flower(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название цветка")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")
    image = models.ImageField(upload_to='flowers/', verbose_name="Изображение цветка")
    description = models.TextField(blank=True, verbose_name="Описание")
    available = models.BooleanField(default=True, verbose_name="Доступен для заказа")

    def __str__(self):
        return self.name


class Bouquet(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='bouquets/')
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    decor = models.CharField(max_length=50, choices=[('ribbon', 'Ленты'), ('box', 'Коробка'), ('garland', 'Гирлянда')],
                             blank=True)
    vase = models.CharField(max_length=50, choices=[('ceramic', 'Керамика'), ('glass', 'Стекло')], blank=True)
    delivery_date = models.CharField(max_length=50,
                                     choices=[('same_day', 'В тот же день'), ('next_day', 'На следующий день')],
                                     blank=True)
    # Фильтры
    flower_type = models.CharField(max_length=50, choices=[
        ('rose', 'Розы'),
        ('lily', 'Лилии'),
        ('daisy', 'Ромашки'),
        ('tulip', 'Тюльпаны')
    ])
    size = models.CharField(max_length=50, choices=[
        ('standard', 'Стандарт'),
        ('deluxe', 'Делюкс'),
        ('premium', 'Премиум')
    ])
    has_discount = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    MANUFACTURER_CHOICES = [
        ('interflora', 'Interflora'),
        ('florafresh', 'Flora Fresh'),
        ('local', 'Местный производитель'),
    ]

    manufacturer = models.CharField(max_length=50, choices=MANUFACTURER_CHOICES, default='local')

    rating = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Рейтинг"
    )

    def __str__(self):
        return self.name


class BouquetFlower(models.Model):
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество цветков")

    def __str__(self):
        return f"{self.flower.name} в {self.bouquet.name}"
