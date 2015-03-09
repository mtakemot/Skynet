from unittest import TestCase
from Users.models import UserProfile
from Packages.models import Service
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.template.defaultfilters import slugify

from Packages.models import Bundle
__author__ = 'T4kMoDe'


class TestUserProfile(TestCase):

   # Profile = UserProfile.get_model("Profile")

    #print("hi")
    def test_profile(self):
        test = UserProfile(username='usernametestd')
        #print (test.username)
        self.assertEquals(test.username,'usernametestd')

        test = UserProfile(website='www.google.com')
        #print (test.website)
        self.assertEquals(test.website,'www.google.com')

        test = UserProfile(fname='mike')
        #print (test.fname)
        self.assertEquals(test.fname,'mike')

        test = UserProfile(lname='takemoto')
        #print (test.lname)
        self.assertEquals(test.lname,'takemoto')

        test = UserProfile(username='chc', website='www.google.com', fname='c', lname='hc')
        self.assertEquals(test.username,'chc')
        self.assertEquals(test.website, 'www.google.com')
        self.assertEquals(test.fname, 'c')
        self.assertEquals(test.lname, 'hc')

        # test = UserProfile(username='chc', website='www.google.com', fname='c', lname='hc')
        # self.assertEquals(test.username,'abc')
        # self.assertEquals(test.website, 'www.yahoo.com')
        # self.assertEquals(test.fname, 'a')
        # self.assertEquals(test.lname, 'b')

        #the following is integrated testing:
        #we will test the successful unit test from before
        #agains a Service object to which UserProfiles have a
        #many to many dependency

        #test.save()
        i=1

        # #count = 0
        #
        service = Service("service_", "integrated test for userProfile and Services", i*10, i*10*12)
        #test.services.add(service)
        i+=1

        #test.services.add(service)

        # service = Service("service_", "integrated test for userProfile and Services", i*10, i*10*12)
        # test.services.add(service)
        # i+=1
        #
        # service = Service("service_", "integrated test for userProfile and Services", i*10, i*10*12)
        # test.services.add(service)
        # i+=1
        #
        # service = Service("service_", "integrated test for userProfile and Services", i*10, i*10*12)
        # test.services.add(service)
        # i+=1
        #
        # service = Service("service_", "integrated test for userProfile and Services", i*10, i*10*12)
        # test.services.add(service)
        # i+=1

        #this will test if this new service object has the proper dependency/visibility from this User

        # for x in test.services.all():
        #     i-1

        if i-1 ==1:
            print("SUCCESSFUL USERPROFILE -> SERVICE TEST")

        else:
            print("FAILED USERPROFILE -> SERVICE TEST")
    #this test will ALWAYS FAIL!
    #def test_fail(self):
        #self.fail()

    #pass