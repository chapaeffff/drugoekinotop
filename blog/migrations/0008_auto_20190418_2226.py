# Generated by Django 2.1.3 on 2019-04-18 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20190418_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film_list_elem',
            name='order',
            field=models.IntegerField(null=True),
        ),
    ]