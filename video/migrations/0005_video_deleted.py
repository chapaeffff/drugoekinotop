# Generated by Django 2.1.3 on 2019-03-01 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0004_remove_video_timeout'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='deleted',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
