# Generated by Django 2.1.3 on 2019-04-18 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20190418_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='compact',
            field=models.BooleanField(default=False),
        ),
    ]