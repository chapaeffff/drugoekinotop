# Generated by Django 2.1.3 on 2019-09-28 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggested', '0005_suggested_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='videosugg',
            name='copyrighted',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]