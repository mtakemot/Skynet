from django.db import models
from django.core.mail import send_mail
from django.conf import settings


# RuleSubject Object functions


#rule to check balance vs threshold and to notify via email if necessary
def balance_notify(self):

    if self.balance > self.threshold:
        send_mail('A COURTESY NOTIFICATION FROM SKYNET: ',
                  'THis is a friendly reminder that your balance has exceeded the threshold value.',
                   settings.EMAIL_HOST_USER,
    [self.userEmail], fail_silently=False)


    if self.balance < 0:
        print("@ RuleSubject.models.balance_notify: Balance cannot be < 0 ")
        self.balance = 0


def update_bundle(self):
    temp_price = self.price
    temp_term = self.term_fee
    self.price = 0
    self.term_fee = 0
    p = 0
    t = 0
    #list = self.bundle_services

    #for x in list:
       #p+=x.price

    # for x in self.bundle_services:
    #     self.price += x.price
    #     self.term_fee += x.term_fee
    # if temp_price !=self.price:
    #     print("new set of services in bundle, updating bundle price")
    # elif temp_term != self.term_fee:
    #     print("new quantity of services, updating cancelation fee n * $150")
    # else:
    #     print("same old and current bundle, no change in price")

    print("updated bundle is now saving!!")