# Generated by Django 4.2.2 on 2023-07-13 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_remove_cartitem_unit_price'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('product', 'cart')},
        ),
    ]