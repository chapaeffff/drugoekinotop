# Generated by Django 2.1.3 on 2019-05-24 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0005_auto_20190419_2356'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/shots/')),
                ('description', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]