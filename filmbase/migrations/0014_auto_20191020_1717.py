# Generated by Django 2.1.3 on 2019-10-20 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmbase', '0013_film_yohoho'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='yohoho',
            field=models.BooleanField(default=True),
        ),
    ]