from django.test import TestCase
from django.core import management

from models import SampleModel


class MigrationTest(TestCase):

    def test_revert(self):
        # Add some data
        SampleModel.objects.create(int_field=1, char_field='hello', text_field='world')
        SampleModel.objects.create(int_field=2, char_field='Mark', text_field='Twain')
        SampleModel.objects.create(int_field=3, char_field='Pink Floyd', text_field='The Dark Side of the Moon')
        # All migrations were run forward automatically, so we just need to check the reverse
        # management.call_command('migrate', 'sample_app', '0001', interactive=False)

