# Generated by Django 2.1.3 on 2019-04-30 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('concept', '0003_auto_20190429_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=200)),
                ('concept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='concept.Concept')),
            ],
        ),
        migrations.RemoveField(
            model_name='connectionfilm',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='connectionfilm',
            name='concept',
        ),
        migrations.RemoveField(
            model_name='connectionfilm',
            name='id',
        ),
        migrations.RemoveField(
            model_name='connectiontag',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='connectiontag',
            name='concept',
        ),
        migrations.RemoveField(
            model_name='connectiontag',
            name='id',
        ),
        migrations.RemoveField(
            model_name='connectionvkpost',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='connectionvkpost',
            name='concept',
        ),
        migrations.RemoveField(
            model_name='connectionvkpost',
            name='id',
        ),
        migrations.AddField(
            model_name='connectionfilm',
            name='connection_ptr',
            field=models.OneToOneField(auto_created=True, default=None, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='concept.Connection'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='connectiontag',
            name='connection_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='concept.Connection'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='connectionvkpost',
            name='connection_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='concept.Connection'),
            preserve_default=False,
        ),
    ]
