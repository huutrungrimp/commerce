# Generated by Django 3.1.2 on 2020-11-10 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0025_remove_comment_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='listing_pics',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
