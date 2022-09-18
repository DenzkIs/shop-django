from django.db import models
from PIL import Image
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Profile
from django.utils import timezone


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Категория товара')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Printer(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория товара')
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(default="default.png", upload_to="printer_pics")
    color = models.BooleanField(default=True, verbose_name='Цветной')

    def __str__(self):
        return f'{self.cat} : {self.title}'

    # def save(self, **kwargs):
    #     super().save(**kwargs)
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 450:
    #         output_size = (300, 450)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

    def get_absolute_url(self):
        return reverse("printer-detail", kwargs={"slug": self.slug})


class Toner(models.Model):

    COLOR_CHOICES = (
        ('C', 'Cyan'),
        ('M', 'Magenta'),
        ('Y', 'Yellow'),
        ('K', 'Black'),
    )

    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория товара', default=2)
    prtr = models.ForeignKey(Printer, on_delete=models.CASCADE, default=1, verbose_name='Подходит для', related_name='toner_printer')
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(default="default.png", upload_to="toner_pics")
    weight = models.DecimalField(max_digits=4, decimal_places=0, verbose_name='Вес')
    color = models.CharField(max_length=1, choices=COLOR_CHOICES, default='K', verbose_name='Цвет')

    def __str__(self):
        return f'{self.cat} : {self.title}'


class Cart(models.Model):

    owner = models.ForeignKey(Profile, verbose_name='Владелец', on_delete=models.CASCADE)
    product = models.ManyToManyField('CartProduct', blank=True, related_name='related_cart')
    total_qty = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Общая цена')
    # delivery = models.BooleanField(default=False, verbose_name='Нужна доставка?')
    time_create = models.DateTimeField(default=timezone.now)
    in_order = models.BooleanField(default=False)
    for_anon_user = models.BooleanField(default=False)

    def __str__(self):
        return str(f'Корзина для {self.owner}')

    def save(self, *args, **kwargs):
        cart_data = self.product.aggregate(models.Sum('final_price'), models.Count('id'))
        if cart_data.get('final_price__sum'):
            self.final_price = cart_data['final_price__sum']
        else:
            self.final_price = 0
        self.total_qty = cart_data['id__count']
        super().save(*args, **kwargs)



class CartProduct(models.Model):

    user = models.ForeignKey(Profile, verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_product')
    product_toner = models.ForeignKey(Toner, on_delete=models.CASCADE, verbose_name='Тонер в корзине')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return f'Продукт: {self.product_toner.title} для корзины {self.user}'

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product_toner.price
        super().save(*args, **kwargs)

