# Generated by Django 3.2.6 on 2021-11-04 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bids',
            old_name='user',
            new_name='winner',
        ),
    ]
