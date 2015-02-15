from django.db import models

# Create your models here.
class Username(models.Model):
    user_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Password(models.Model):
    password = models.ForeignKey(Username)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)