# Generated by Django 3.2.6 on 2021-11-02 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctions',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
