from django.db import models

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=250)
    price = models.IntegerField(default=0)
    term_fee = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Bundle(models.Model):
    name = models.CharField(max_length=123, unique=True)
    description = models.CharField(max_length=250)
    price = models.IntegerField(default=0)
    term_fee = models.IntegerField(default=0)
    bundle_services = models.ManyToManyField(Service, blank=True, )

#class AllService(models.Model):
#class Package(models.Model):
    #services = models.ManyToOneRel(Service)
