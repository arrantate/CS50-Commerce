# Generated by Django 3.1.5 on 2021-01-31 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20210131_1156'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishlist',
            old_name='item',
            new_name='items',
        ),
    ]
