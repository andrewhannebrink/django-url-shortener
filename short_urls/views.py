from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from short_urls.models import Short_URL, Custom_URL
from short_urls.serializers import Short_URL_Serializer, Custom_URL_Serializer
import random

def last_hundred(request):
   return HttpResponse('This is the api/last_hundred endpoint')

def shortened_url_view(request):
   return HttpResponse('This url is not yet a shortened url')

@api_view(['POST'])
def make_short(request):
    if request.method == 'POST':
        long_url_exists = False #TODO dynamically find long_url in Short_URL models
        if long_url_exists == False:
            long_url = request.data['long_url']
            short_url = makeShortURL()
            domain = 'test.domain'
            number_visits = 0
            time_stamp = '1991-04-18 07:00'
            new_url_obj = Short_URL.objects.create(long_url=long_url, short_url=short_url, domain=domain, time_stamp=time_stamp, number_visits=number_visits)
            new_url_obj.save()
            response = {'short_url': short_url, 'message': 'success, Short_URL object created'}
        else:
            response = {'message': 'long url already exists in database'}
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
    ri = random.randint(0, l - 1)
    s = ''
    for i in range(6):
        s += poss[ri]
    return s
