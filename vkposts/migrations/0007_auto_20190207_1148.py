# Generated by Django 2.1.3 on 2019-02-07 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vkposts', '0006_auto_20190207_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='vkpost',
            name='blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vkpost',
            name='side_video',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]