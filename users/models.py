from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, verbose_name='Название компании')
    address = models.CharField(max_length=255, verbose_name='Адрес доставки')
    discount = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Скидка', default=0)

    def __str__(self):
        return f'{self.user.username} Профиль'
