# Generated by Django 2.1.3 on 2019-02-12 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vkposts', '0008_vkpost_copy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vkpost',
            name='reposts',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]