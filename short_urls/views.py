from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from short_urls.models import Short_URL, Custom_URL
from short_urls.serializers import Short_URL_Serializer, Custom_URL_Serializer
from django.db.models import Count
import random
import datetime
#from urlparse import urlparse
import tldextract

# (2) api/last_hundred endpoint
# API endpoint for checking the last 100 most recently shortened urls
@api_view(['GET'])
def last_hundred(request):
    if request.method == 'GET':
        ordered = Short_URL.objects.order_by('time_stamp')
        if len(ordered) >= 100:
            top = ordered[-100:].reverse()
        else:
            top = ordered.reverse()
        l = len(top)
        response = {'top': []}
        for obj in top:
            response['top'].append({
                'long_url': obj.long_url,
                'short_url': obj.short_url,
                'time_stamp': obj.time_stamp
            })
        return Response(response, status=status.HTTP_200_OK)
        
# (3) api/domains endpoint
# API Endpoint for retrieving the domains with the most associated shortened urls
@api_view(['GET'])
def domains(request):
    if request.method == 'GET':
        ordered = Short_URL.objects.values('domain').annotate(num_urls = Count('domain')).order_by('-num_urls')
        if len(ordered) >= 10:
            top = ordered[-10:] 
        else:
            top = ordered
        l = len(top)
        response = {'top': []}
        for obj in top:
            response['top'].append(obj)
        return Response(response, status=status.HTTP_200_OK)


# (6) \w* endpoint
# API endpoint for redirecting to a long_url at a custom or short url 
def shortened_url_view(request):
   return HttpResponse('This url is not yet a shortened url')

# (1) /api/make_short endpoint
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
            short_url_obj = Short_URL.objects.get(long_url = request.data['long_url'])
            short_url_obj.time_stamp = str(datetime.datetime.now())
            short_url_obj.save()
            response = {'message': 'long_url already exists in database...updated entry\'s time_stamp'}
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
