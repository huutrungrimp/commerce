# Generated by Django 3.1.2 on 2020-11-01 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_remove_bid_bidprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidlisting',
            name='bidprice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
