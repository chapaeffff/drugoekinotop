# Generated by Django 2.1.3 on 2019-10-20 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmbase', '0012_film_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='yohoho',
            field=models.BooleanField(default=False),
        ),
    ]