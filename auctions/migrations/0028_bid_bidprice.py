# Generated by Django 3.1.2 on 2020-11-11 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0027_auto_20201111_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='bidprice',
            field=models.FloatField(null=True),
        ),
    ]
