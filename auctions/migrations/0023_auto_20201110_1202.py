# Generated by Django 3.1.2 on 2020-11-10 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_auto_20201110_1157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='content',
        ),
    ]