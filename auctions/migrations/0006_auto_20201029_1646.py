# Generated by Django 3.1.2 on 2020-10-29 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_bidlisting_bidprice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bidlisting',
            name='bidprice',
        ),
        migrations.AddField(
            model_name='bid',
            name='bidprice',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True),
        ),
    ]
