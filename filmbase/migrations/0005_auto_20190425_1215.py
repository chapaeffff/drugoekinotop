# Generated by Django 2.1.3 on 2019-04-25 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmbase', '0004_auto_20190425_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='director',
            name='kp_id',
            field=models.PositiveIntegerField(default=0, unique=True),
            preserve_default=False,
        ),
    ]
