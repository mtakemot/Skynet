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

        test = UserProfile(website='www.google.com')
        print (test.website)
        self.assertEquals(test.website,'www.google.com')

        test = UserProfile(fname='mike')
        print (test.fname)
        self.assertEquals(test.fname,'mike')

        test = UserProfile(lname='takemoto')
        print (test.lname)
        self.assertEquals(test.lname,'takemoto')

    #this test will ALWAYS FAIL!
    def test_fail(self):
        self.fail()

    pass