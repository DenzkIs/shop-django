# Generated by Django 4.1 on 2022-09-06 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_printer_image_toner_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='toner',
            name='weight',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=4, verbose_name='Вес'),
            preserve_default=False,
        ),
    ]
