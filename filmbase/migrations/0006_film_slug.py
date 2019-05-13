# Generated by Django 2.1.3 on 2019-05-13 09:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('filmbase', '0005_auto_20190425_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='slug',
            field=models.SlugField(default=uuid.uuid4, max_length=200, null=True),
        ),
    ]
