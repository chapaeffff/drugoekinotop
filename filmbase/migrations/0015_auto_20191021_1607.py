# Generated by Django 2.1.3 on 2019-10-21 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmbase', '0014_auto_20191020_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='kodik',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='film',
            name='last_kodik_search',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
