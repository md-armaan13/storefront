# Generated by Django 4.2.2 on 2023-06-26 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_collection_options_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['first_name', 'last_name']},
        ),
        migrations.RemoveIndex(
            model_name='customer',
            name='store_custo_last_na_2e448d_idx',
        ),
    ]
