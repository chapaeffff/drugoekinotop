# Generated by Django 2.1.3 on 2019-05-29 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmbase', '0009_film_moratory10'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='profit_russia',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='film',
            name='profit_usa',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='film',
            name='release',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]