# Generated by Django 2.1.3 on 2019-02-13 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vkposts', '0010_auto_20190212_1639'),
        ('suggested', '0009_auto_20190213_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggested',
            fields=[
                ('vkpost_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vkposts.VKPost')),
                ('from_id', models.PositiveIntegerField(blank=True)),
                ('rating', models.PositiveSmallIntegerField(default=1)),
            ],
            bases=('vkposts.vkpost',),
        ),
    ]
