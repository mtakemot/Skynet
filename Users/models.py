from django.db import models
from django.contrib.auth.models import User, UserManager
from django.template.defaultfilters import slugify
from Packages.models import Service as serviceModels
from Packages.models import Bundle as bundleModels
from Rule.models import BusinessRules


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) #changes whitespace to hyphens
        super(Category,self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

#creating an observer design's subject interface:

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    username = models.CharField(max_length=20, primary_key=True)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    fname = models.CharField(max_length=20, blank=True, verbose_name="First Name") #user first name
    lname = models.CharField(max_length=20, blank=True, verbose_name="Last Name") #user last name
    userEmail = models.CharField(max_length=45, blank=True) #REQUIRED FOR AUTOEMAIL SERVICES
    services = models.ManyToManyField(serviceModels, blank=True)
    bundles = models.ManyToManyField(bundleModels, blank=True)

    #Follow is for customer's current balance, and balance threshold (for notifications)
    balance = models.IntegerField(max_length=9, default=0)
    threshold = models.IntegerField(max_length=9, default=0)

    is_Market = models.BooleanField(default=False)
    is_Service = models.BooleanField(default=False)


    def get_services(self):
        return "\n".join([p.name for p in self.services.all()])

    # override save, b/c any change in a field will always save in DB using Django framework.
    # override so that before the actual userprofileobject.save() occurs,
    # check balance vs threshold and use rule obj method to verify if a notification
    # needs to be sent or not. Then, call userprofileobject.save()
    def save(self):
        instance = BusinessRules()
        #instance.balance_notify(self)


        super(UserProfile,self).save()
        #super(UserProfile, self).save(force_insert=True, force_update=False)



def UserFactory(newUser):
    profile=UserProfile(user=newUser, username=newUser, fname=newUser.first_name,
                                   lname=newUser.first_name, userEmail=newUser.email, website=newUser.website)
    return profile

# class UserFactory(User):
#     current_profile = models.OneToOneField(UserProfile)
#
#
#
#
#     def __init__(self, user):
#         self.current_profile = UserProfile(user=self.user, username=self.user.name,fname=self.first_name,
#                                    lname=self.first_name, userEmail=self.email, website=self.website)
#
#         print("testing factory, USER first name: ", self.current_profile.fname)
#         #current_user.save()
#
#     def save(self):
#         print("saving this factory's generated UserProfile")
#         self.current_profile.save()
#         return self.current_profile
#
#     #def check_permission(self):
#         #if self.is_Market:
#             #return HttpResponseRedirect('/Users/market_rep')
#
#
#
#
#     # Override the __unicode__() method to return out something meaningful!
#     def __str__(self):
#         return 'Name: %s %s UserName: %s' % (self.fname, self.lname, self.username)

