# Generated by Django 2.1.3 on 2019-05-13 09:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('filmbase', '0010_auto_20190513_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='slug',
            field=models.SlugField(default=uuid.uuid1, max_length=200),
        ),
    ]
