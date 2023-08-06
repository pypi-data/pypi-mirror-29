from unittest import TestCase

from io import StringIO

from aare.aare import aare
from aare.tests.utils import capture_streams, cli_arguments, SessionMock


class TestAare(TestCase):
    def test_does_not_crash(self):
        with self.assertRaises(SystemExit) as cm:
            aare()
        self.assertEqual(0, cm.exception.code)

    def test_prints_temperature(self):
        stdout = StringIO()
        with capture_streams(stdout=stdout), self.assertRaises(SystemExit):
            with SessionMock().expect_get('http://aare.schwumm.ch/aare.json', 'current_temperature.json'):
                aare()
        self.assertEqual('Current temperature of the aare: 5.4° C\n', stdout.getvalue())

    def test_prints_temperature_ger(self):
        stdout = StringIO()
        with capture_streams(stdout=stdout), cli_arguments('--language de'), self.assertRaises(SystemExit):
            with SessionMock().expect_get('http://aare.schwumm.ch/aare.json', 'current_temperature.json'):
                aare()
        self.assertEqual('Aktuelle Temperatur der Aare: 5.4° C\n', stdout.getvalue())
