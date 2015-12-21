from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from short_urls.models import Short_URL, Custom_URL
from short_urls.serializers import Short_URL_Serializer, Custom_URL_Serializer
import random
import datetime
#from urlparse import urlparse
import tldextract

def last_hundred(request):
   return HttpResponse('This is the api/last_hundred endpoint')

def shortened_url_view(request):
   return HttpResponse('This url is not yet a shortened url')

#/api/make_short endpoint
# API endpoint for making a new shortened url given a long url
@api_view(['POST'])
def make_short(request):
    if request.method == 'POST':
        # Check to see if short_url entry with provided long_url exists
        res_len = Short_URL.objects.filter(long_url = request.data['long_url']).count()
        if res_len == 0:
            long_url_exists = False
        else:
            long_url_exists = True
        # If long_url doesn't exist yet, make new short_url obj and save
        if long_url_exists == False:
            long_url = request.data['long_url']
            short_url = makeShortURL()
            tld = tldextract.extract(long_url)
            domain = tld.domain + '.' + tld.suffix
            number_visits = 0
            time_stamp = str(datetime.datetime.now())
            new_url_obj = Short_URL.objects.create(long_url=long_url, short_url=short_url, domain=domain, time_stamp=time_stamp, number_visits=number_visits)
            new_url_obj.save()
            response = {'short_url': short_url, 'domain': domain, 'message': 'success, Short_URL object created'}
        #If long_url already exists, respond with an appropriate message, and do nothing
        else:
            response = {'message': 'long_url already exists in database'}
        #serializer = Short_URL_Serializer(data = request.data)
        #if serializer.is_valid():
        #    serializer.save()
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(response, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# makes random url string of length 6 
def makeShortURL():
    poss = '0123456789abcdefghijklmnopqrstuvwxyz'
    l = len(poss)
    s = ''
    for i in range(6):
        ri = random.randint(0, l - 1)
        s += poss[ri]
    # If short_url already exists (even as a custom url), make a new short_url, else, return s
    short_url_count = Short_URL.objects.filter(short_url = s).count()
    custom_url_count = Custom_URL.objects.filter(custom_url = s).count()
    if (short_url_count + custom_url_count) > 0:
        return makeShortURL() 
    return s 
