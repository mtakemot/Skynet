from unittest import TestCase
from Users.models import UserProfile
from Packages.models import Service
__author__ = 'T4kMoDe'


class TestUserProfile(TestCase):
    print("hi")
    def test_profile(self):
        test = UserProfile(username='usernametestd')
        print (test.username)
        self.assertEquals(test.username,'usernametestd')

    #this test will ALWAYS FAIL!
    def test_fail(self):
        self.fail()

    pass