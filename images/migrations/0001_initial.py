# Generated by Django 2.1.3 on 2019-04-17 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filmbase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('film', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='filmbase.Film')),
            ],
        ),
    ]