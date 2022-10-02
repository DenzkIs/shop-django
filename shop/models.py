from PIL import Image
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Profile
from django.utils import timezone
from django.db import models
from .utils import currency

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
    specification = models.FileField(default="default.pdf", upload_to="printer_manuals")
    color = models.BooleanField(default=True, verbose_name='Цветной')
    show_main = models.BooleanField(default=False, verbose_name='Показывать на главной')


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
    total_qty = models.PositiveIntegerField(default=0) # это поле решил не использовать
    final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Общая цена') # это поле решил не использовать
    time_create = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(f'Корзина для {self.owner}')


    # При создании корзины вылетали ошибки

    # def save(self, *args, **kwargs):
    #     # super().save(*args, **kwargs)
    #     cart_data = self.product.aggregate(models.Sum('final_price'), models.Count('id'))
    #     if cart_data.get('final_price__sum'):
    #         self.final_price = cart_data['final_price__sum']
    #     else:
    #         self.final_price = 0
    #     self.total_qty = cart_data['id__count']
    #     super().save(*args, **kwargs)

    @property
    def f_price(self):
        cart_data = self.product.aggregate(models.Sum('final_price'), models.Count('id'))
        if cart_data.get('final_price__sum'):
            self.final_price = cart_data['final_price__sum']
        else:
            self.final_price = 0
        return self.final_price




class CartProduct(models.Model):

    user = models.ForeignKey(Profile, verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_product')
    product_toner = models.ForeignKey(Toner, on_delete=models.CASCADE, verbose_name='Тонер в корзине')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')


    def __str__(self):
        return f'Продукт: {self.product_toner.title} для корзины {self.user}'

    def save(self, *args, **kwargs):
        self.final_price = self.qty * float(self.product_toner.price) * float(self.user.discount) * currency['euro_ex_rate']
        super().save(*args, **kwargs)

    @property
    def discount_price(self):
        return self.final_price / self.qty


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    DELIVERY_NEED = 'need'
    DELIVERY_PICKUP = 'pickup'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый'),
        (STATUS_IN_PROGRESS, 'В обработке'),
        (STATUS_READY, 'Готов к отгрузке'),
        (STATUS_COMPLETED, 'Выполнен')
    )

    DELIVERY_CHOICES = (
        (DELIVERY_NEED, 'Нужна доставка'),
        (DELIVERY_PICKUP, 'Самовывоз')
    )

    customer = models.ForeignKey(Profile, verbose_name='Покупатель', related_name='related_orders', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(max_length=100, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_NEW)
    delivery = models.CharField(max_length=100, verbose_name='Тип доставки', choices=DELIVERY_CHOICES, default=DELIVERY_PICKUP)
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(default=timezone.now, verbose_name='Дата доставки (самовывоза) заказа')

    def __str__(self):
        return f'Заказ №{self.id} ({self.customer})'


