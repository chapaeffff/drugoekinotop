# Generated by Django 2.1.3 on 2019-04-18 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_author_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='finished',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='list',
            name='publish',
            field=models.BooleanField(default=True),
        ),
    ]