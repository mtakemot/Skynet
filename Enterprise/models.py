from django.db import models
from Rule.models import BusinessRules
from Packages.models import Service, Bundle
from Users.models import UserProfile

# Enterprise component design Facade and mediator
class Facade_Enterprise:
    userAccounts= models.ManyToManyField(UserProfile, blank=True)
    services = models.ManyToManyField(Service, blank=True)
    bundles = models.ManyToManyField(Bundle, blank=True)
    rules = models.OneToOneField(BusinessRules, blank=True)

    def __init__(self):
        pass

    def delete(self):
        pass

    def print_all_objects(self):
        pass


#mediator for sub component handling
class Enterprise(Facade_Enterprise):

    def __init__(self):
        for x in UserProfile.objects.all():
            self.userAccounts.add(x)
        for x in Service.objects.all():
            self.services.add(x)
        for x in Bundle.objects.all():
            self.bundles.add(x)

        self.rules = BusinessRules

    def delete(dataType, self):
        if self is None:
            print("please enter a valid object instance to delete")
            return

        if dataType == UserProfile:
            x = UserProfile.objects.get(self)
            x.delete()
            UserProfile.save()
            self.save()

        elif dataType == Service:
            x = Service.objects.get(self)
            x.delete()
            Service.save()
            self.save()

        elif dataType== Bundle:
            x = Bundle.objects.get(self)
            x.delete()
            Bundle.save()
            self.save()

        elif dataType==BusinessRules:
            x = BusinessRules.objects.get(self)
            x.delete()
            BusinessRules.save()
            self.save()

        else:
            print("please enter a correct object type to delete")



