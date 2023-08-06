# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from infi.django_postgresql_migrations.operations import SetStatistics


class Migration(migrations.Migration):

    dependencies = [
        ('sample_app', '0003_create_trigram_index'),
    ]

    operations = [
        SetStatistics('SampleModel', 'int_field'),
        SetStatistics('SampleModel', 'char_field', 500),
    ]
