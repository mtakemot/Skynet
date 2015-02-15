from django.db import models

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=250)
    price = models.IntegerField(default=0)
    term_fee = models.IntegerField(default=0)

    def __str__(self):
        return self.name


#class Package(models.Model):
    #services = models.ManyToOneRel(Service)
