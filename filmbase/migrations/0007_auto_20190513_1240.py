# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import uuid

def gen_slug(apps, schema_editor):
    Film = apps.get_model('filmbase', 'Film')
    for row in Film.objects.all():
        row.slug = uuid.uuid4()
        row.save()


class Migration(migrations.Migration):

    dependencies = [
        ('filmbase', '0006_film_slug'),
    ]

    operations = [
        # omit reverse_code=... if you don't want the migration to be reversible.
        migrations.RunPython(gen_slug, reverse_code=migrations.RunPython.noop),
    ]
