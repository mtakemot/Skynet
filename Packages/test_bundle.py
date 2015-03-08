from unittest import TestCase
from Packages.models import Bundle, Service
__author__ = 'T4kMoDe'


class TestBundle(TestCase):



    def test_get_services(self):

        strng = str(10)
        test = Bundle(name='hello', description='buy me', price=10, term_fee=150, )
        self.assertEquals(test.name, "hello")
        self.assertEquals(test.price, strng)
        self.fail()

    def test_save(self):
        self.fail()