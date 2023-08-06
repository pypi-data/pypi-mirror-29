from unittest import TestCase
from mlx.json_to_mako import json_to_mako_wrapper


class TestJsonToMako(TestCase):

    def test_help(self):
        with self.assertRaises(SystemExit) as ex:
            json_to_mako_wrapper(['--help'])
        self.assertEqual(0, ex.exception.code)

    def test_version(self):
        with self.assertRaises(SystemExit) as ex:
            json_to_mako_wrapper(['--version'])
        self.assertEqual(0, ex.exception.code)

    def test_example_single_input(self):
        json_to_mako_wrapper(['--input', 'example/family.json',
                              '--input', 'example/work.json',
                              '--template', 'example/address-book.mako',
                              '--output', 'tests/address-book.html'])

    def test_example_dual_input(self):
        json_to_mako_wrapper(['--input', 'example/family.json',
                              '--template', 'example/address-book.mako',
                              '--output', 'tests/address-book.html'])

    def test_example_no_input(self):
        with self.assertRaises(SystemExit) as ex:
            json_to_mako_wrapper(['--template', 'example/address-book.mako',
                                  '--output', 'tests/address-book.html'])
        self.assertEqual(2, ex.exception.code)

    def test_example_no_template(self):
        with self.assertRaises(SystemExit) as ex:
            json_to_mako_wrapper(['--input', 'example/family.json',
                                  '--input', 'example/work.json',
                                  '--output', 'tests/address-book.html'])
        self.assertEqual(2, ex.exception.code)

    def test_example_no_output(self):
        with self.assertRaises(SystemExit) as ex:
            json_to_mako_wrapper(['--input', 'example/family.json',
                                  '--input', 'example/work.json',
                                  '--template', 'example/address-book.mako'])
        self.assertEqual(2, ex.exception.code)
