# Generated by Django 2.1.3 on 2019-02-12 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggested', '0002_auto_20190212_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggested',
            name='from_id',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]