from django.db import models
from PIL import Image
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Категория товара')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Printer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория товара')
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(default="default.png", upload_to="printer_pics")
    color = models.BooleanField(default=True, verbose_name='Цветной')

    def __str__(self):
        return f'{self.category} : {self.title}'

    def save(self, **kwargs):
        super().save(**kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 450:
            output_size = (300, 450)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse("printer-detail", kwargs={"slug": self.slug})


class Toner(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(default="default.png", upload_to="toner_pics")
    weight = models.DecimalField(max_digits=4, decimal_places=0, verbose_name='Вес')

    def __str__(self):
        return f'{self.category} : {self.title}'

    def save(self, **kwargs):
        super().save(**kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 450:
            output_size = (300, 450)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Profile(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)