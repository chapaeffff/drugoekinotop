# Generated by Django 2.1.3 on 2019-07-04 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concept', '0006_concept_calc_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='concept',
            name='full',
            field=models.BooleanField(default=True),
        ),
    ]