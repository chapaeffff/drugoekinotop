# Generated by Django 2.1.3 on 2019-10-20 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_film_list_elem_maybe'),
    ]

    operations = [
        migrations.AddField(
            model_name='film_list_elem',
            name='to_drop',
            field=models.BooleanField(default=False),
        ),
    ]
