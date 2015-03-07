from django.db import models

# Rule Object functions


#rule to check balance vs threshold and to notify via email if necessary
def balance_check(self):

    if self.balance > self.threshold:

            print("BALANCE EXCEEDS THRESHOLD! PAY UP!!")
    if self.balance < 0:
        print("@ Rule.models.balance_check: Balance cannot be < 0 ")
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