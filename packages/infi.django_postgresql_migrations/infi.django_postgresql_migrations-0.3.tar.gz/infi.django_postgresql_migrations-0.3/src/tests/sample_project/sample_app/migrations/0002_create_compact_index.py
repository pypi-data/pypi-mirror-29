# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from infi.django_postgresql_migrations.operations import CreateCompactIndex


class Migration(migrations.Migration):

    dependencies = [
        ('sample_app', '0001_initial'),
    ]

    operations = [
        CreateCompactIndex('SampleModel', 'int_field'),
        CreateCompactIndex('SampleModel', 'char_field', 'my_index'),
        CreateCompactIndex('SampleModel', 'char_field', 'my_partial_index', where='length(char_field) < 4'),
        CreateCompactIndex('SampleModel', ['int_field', 'char_field'], where='length(char_field) < 4')
    ]
