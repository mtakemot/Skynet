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

        test = Bundle(name='bundle1', description='good', price=20, term_fee=500 )
        self.assertEquals(test.name, "bundle1")
        self.assertEquals(test.description, 'good')
        self.assertEquals(test.price, '20')
        self.assertEquals(test.term_fee, '500')

        test = Bundle(name='bundle2', description='great', price=30, term_fee=350)
        self.assertEquals(test.name, "bundle2")
        self.assertEquals(test.description, 'great')
        self.assertEquals(test.price, '30')
        self.assertEquals(test.term_fee, 350)

        test = Bundle(name='bundle3', description='best', price=50, term_fee=90)
        self.assertEquals(test.name, "bundle2")
        self.assertEquals(test.description, 'great')
        self.assertEquals(test.price, '30')
        self.assertEquals(test.term_fee, 350)

        test = Bundle(name='bundle4', description='value', price=9, term_fee=450)
        self.assertEquals(test.name, "bundle2")
        self.assertEquals(test.description, 'great')
        self.assertEquals(test.price, '30')
        self.assertEquals(test.term_fee, 350)
    def test_save(self):
        self.fail()