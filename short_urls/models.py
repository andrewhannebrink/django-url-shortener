from __future__ import unicode_literals

from django.db import models

# Class defining the Short_URL model - creates 1:1 mapping of short urls to long urls
class Short_URL(models.Model):
   long_url = models.CharField(max_length=300)
   domain = models.CharField(max_length=100)
   short_url = models.CharField(max_length=6)
   number_visits = models.IntegerField(default=0)
   time_stamp = models.DateTimeField('date shortened')

   
# Class for Custom_URL model - each Custom_URL refers to a Short_URL model object 
class Custom_URL(models.Model):
   short_url = models.ForeignKey(Short_URL, on_delete=models.CASCADE)
   custom_url = models.CharField(max_length=50)
