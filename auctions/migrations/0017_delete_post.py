# Generated by Django 3.1.2 on 2020-11-09 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_post'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]