# Generated by Django 4.1 on 2022-10-05 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_profile_discount_profile_discount_percent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='discount_percent',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Скидка (%)'),
        ),
    ]
