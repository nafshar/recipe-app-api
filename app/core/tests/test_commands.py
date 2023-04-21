"""
Test custom Django management command
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """ Test Commands"""

    def test_wait_for_db_ready(self, patched_check):
        """ Test is DB is up and ready """
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """ Test waiting for DB, when getting Operational Error
            The line below is one which was imperically developed
            by Mark at Udemy, He tried this several times and
            decided on how to implement this method with these numbers
            of 2 & 3. They can be arbitarily changed to any number.
            They represent how many times each exception could be raised.
        """
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])

