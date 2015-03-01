from unittest import TestCase
from Packages.models import Service
__author__ = 'T4kMoDe'


class TestService(TestCase):
    def test_service(self):
        test = Service(name='package 2')
        print (test.name)
        self.assertEquals(test.name,'package 2')

        test = Service(description='unit test package 2')
        print (test.description)
        self.assertEquals(test.description,'unit test package 2')

        test = Service(price=69.99)
        print (test.price)
        self.assertEquals(test.price,69.99)



    def test_service_termination(self):
        test = Service(term_fee=199.99)
        print (test.term_fee)
        self.assertEquals(test.term_fee,199.99)

    #this test will ALWAYS FAIL!
    def test_fail(self):
        self.fail()
    pass

