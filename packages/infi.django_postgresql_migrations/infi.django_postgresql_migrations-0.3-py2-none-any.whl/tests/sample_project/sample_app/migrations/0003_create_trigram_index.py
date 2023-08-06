# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from infi.django_postgresql_migrations.operations import CreateTrigramIndex


class Migration(migrations.Migration):

    dependencies = [
        ('sample_app', '0002_create_compact_index'),
    ]

    operations = [
        CreateTrigramIndex('SampleModel', 'char_field'),
        CreateTrigramIndex('SampleModel', 'text_field', 'my_trgm_index'),
        CreateTrigramIndex('SampleModel', 'text_field', 'my_partial_trgm_index', where='text_field IS NOT NULL')
    ]
