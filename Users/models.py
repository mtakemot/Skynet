from django.db import models
from django.contrib.auth.models import User, UserManager
from django.template.defaultfilters import slugify
from Packages.models import Service as serviceModels
from Packages.models import Bundle as bundleModels
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

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    username = models.CharField(max_length=20, primary_key=True)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    fname = models.CharField(max_length=20, blank=True, verbose_name="First Name") #user first name
    lname = models.CharField(max_length=20, blank=True, verbose_name="Last Name") #user last name
    userEmail = models.CharField(max_length=45, blank=True) #user email
    services = models.ManyToManyField(serviceModels, blank=True)
    bundles = models.ManyToManyField(bundleModels, blank=True)
    is_Market = models.BooleanField(default=False)


    def get_services(self):
        return "\n".join([p.name for p in self.services.all()])

    #def check_permission(self):
        #if self.is_Market:
            #return HttpResponseRedirect('/Users/market_rep')




    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return 'Name: %s %s UserName: %s' % (self.fname, self.lname, self.username)

