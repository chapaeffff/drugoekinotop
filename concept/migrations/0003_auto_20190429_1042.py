# Generated by Django 2.1.3 on 2019-04-29 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concept', '0002_auto_20190429_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connectionfilm',
            name='comment',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='connectiontag',
            name='comment',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='connectionvkpost',
            name='comment',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
