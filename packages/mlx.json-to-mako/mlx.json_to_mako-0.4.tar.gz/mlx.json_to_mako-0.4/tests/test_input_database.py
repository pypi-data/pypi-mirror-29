from unittest import TestCase
from mlx.json_to_mako import InputDatabase, to_identifier


class TestInputDatabase(TestCase):

    def test_ok(self):
        db = InputDatabase('example/family.json')
        self.assertEqual('example/family.json', db.source)
        self.assertEqual('family', db.name)
        self.assertIsNotNone(db.data)


class TestToIdentifier(TestCase):

    def test_to_identifier(self):
        name = to_identifier('#f$a@!%m^i&(l )+=y')
        self.assertEqual('family', name)
        name = to_identifier('#_f$a@!%m^i&(l )+=y')
        self.assertEqual('_family', name)
