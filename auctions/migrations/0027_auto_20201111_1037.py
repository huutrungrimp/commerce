# Generated by Django 3.1.2 on 2020-11-11 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0026_listing_listing_pics'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='listings',
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]
