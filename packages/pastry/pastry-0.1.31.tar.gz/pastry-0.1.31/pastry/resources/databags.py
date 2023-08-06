'''Databdg provides the methods for chef databags'''

from .base import Base
from pastry.pastry_client import PastryClient


class Databags(Base):
    '''
    Provides methods for interacting with chef cookbooks
    '''
    _base_url = '/organizations/%(org)s/data'

    @classmethod
    def index(cls):
        '''
        Fetches all of the cookbooks (and versions) on the chef server

        :return: All the chef cookbooks and versions
        :rtype: hash
        '''
        return super(Databags, cls).index()

    @classmethod
    def get_item(cls, databagid, itemid):
        '''
        Fetch a databag item from the chef server

        :param databagid: The databag's name
        :type databagid: string
        :param itemid: The item name
        :type itemid: string
        :return: The databag item
        :rtype: hash
        '''
        return PastryClient.call('%s/%s/%s' % (cls.base_url(), databagid, itemid))

    @classmethod
    def create_item(cls, databagid, item):
        '''
        Create a databag item on the chef server

        :param databagid: The databag's name
        :type databagid: string
        :param item: The item hash
        :type item: hash
        :return: The databag item
        :rtype: hash
        '''
        return PastryClient.call('%s/%s' % (cls.base_url(), databagid), method='POST', data=item)

    @classmethod
    def delete_item(cls, databagid, itemid):
        '''
        Delete a databag item from the chef server

        :param databagid: The databag's name
        :type databagid: string
        :param itemid: The item name
        :type itemid: string
        :return: The databag item
        :rtype: hash
        '''
        return PastryClient.call('%s/%s/%s' % (cls.base_url(), databagid, itemid), method='DELETE')


    @classmethod
    def update_item(cls, databagid, itemid, item):
        '''
        Delete a databag item from the chef server

        :param databagid: The databag's name
        :type databagid: string
        :param itemid: The item name
        :type itemid: string
        :param item: The item hash
        :type item: hash
        :return: The databag item
        :rtype: hash
        '''
        return PastryClient.call('%s/%s/%s' % (cls.base_url(), databagid, itemid), method='PUT', data=item)
