# Generated by Django 4.2.2 on 2023-06-25 05:58

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='taggeditem',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
