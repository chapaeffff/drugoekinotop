# Generated by Django 2.1.3 on 2019-05-30 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmbase', '0011_film_last_search'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='modified',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
