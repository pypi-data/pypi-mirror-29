import mock
import unittest

from pastry.resources.databags import Databags


class DatabagsTestCase(unittest.TestCase):

    @mock.patch('pastry.resources.databags.Base.index', return_value='index')
    def test_index(self, base):
        self.assertEqual(Databags.index(), 'index')

    @mock.patch('pastry.resources.databags.Base.exists', return_value=True)
    def test_exists(self, base):
        self.assertEqual(Databags.exists('group'), True)

    @mock.patch('pastry.resources.databags.PastryClient.call', return_value='item')
    def test_get_item(self, call):
        self.assertEqual(Databags.get_item('databagid', 'itemid'), 'item')

    @mock.patch('pastry.resources.databags.PastryClient.call', return_value='item')
    def test_create_item(self, call):
        self.assertEqual(Databags.create_item('databagid', {}), 'item')

    @mock.patch('pastry.resources.databags.PastryClient.call', return_value='item')
    def test_delete_item(self, call):
        self.assertEqual(Databags.delete_item('databagid', 'itemid'), 'item')

    @mock.patch('pastry.resources.databags.PastryClient.call', return_value='item')
    def test_update_item(self, call):
        self.assertEqual(Databags.update_item('databagid', 'itemid', {}), 'item')
