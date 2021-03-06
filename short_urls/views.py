from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from short_urls.models import Short_URL, Custom_URL
from django.db.models import Count
import random
import datetime
import tldextract


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
            new_url_obj = makeShortURLObj(long_url)
            response = {'short_url': new_url_obj.short_url, 'message': 'success, Short_URL object created'}
        #If long_url already exists, respond with an appropriate message, and do nothing
        else:
            short_url_obj = Short_URL.objects.get(long_url = request.data['long_url'])
            short_url_obj.time_stamp = str(datetime.datetime.now())
            short_url_obj.save()
            response = {'message': 'long_url already exists in database...updated entry\'s time_stamp'}
        return Response(response, status=status.HTTP_200_OK)


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


# (4) api/visits endpoint
# API Endpoint for retrieving how many times a url has been visited given its short_url or custom_url string
@api_view(['POST'])
def visits(request):
    if request.method == 'POST':
        short_url = request.data['short_url']
        filt = Short_URL.objects.filter(short_url = short_url)
        if len(filt) > 0:
            obj = filt[0]
            response = {
                'short_url': obj.short_url,
                'number_visits': obj.number_visits
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'the requested short url has not been created yet'}
            return Response(response, status=status.HTTP_200_OK)

# (5) api/custom endpoint
# API Endpoint for creating custom urls
@api_view(['POST'])
def custom(request):
    if request.method == 'POST':
        # Check that the custom url doesnt already exist
        confirm = confirmAvailableURL(request.data['custom_url'])
        if confirm == False:
            response = {'message': 'suggested custom url is already in use'}
        else:
            # See if the corresponding long_url exists in the short_urls table, if so, use that short_url as foreign key, else, make a new short_url obj and save it
            long_url_list = Short_URL.objects.filter(long_url = request.data['long_url'])
            long_url_count = long_url_list.count()
            if long_url_count > 0:
                obj = long_url_list[0]
                Custom_URL.objects.create(custom_url=request.data['custom_url'], short_url=obj)
                response = {
                    'message': 'custom url created with existing short url alias', 
                    'short_url': obj.short_url,
                    'custom_url': request.data['custom_url'],
                    'long_url': request.data['long_url']
                }
            else:
                # If custom url's requested corresponding long url doesn't exist at all as a short url, make the corresponding short url object along with the new custom url
                obj = makeShortURLObj(request.data['long_url'], banned_names=[request.data['custom_url']])
                cust = Custom_URL.objects.create(custom_url = request.data['custom_url'], short_url=obj) # implicitly calls save()
                cust.short_url = obj
                cust.save()
                response = {
                    'message': 'custom url created with new short url alias', 
                    'short_url': obj.short_url,
                    'custom_url': request.data['custom_url'],
                    'long_url': request.data['long_url']
                }
        return Response(response, status=status.HTTP_200_OK)                 
                

# (6) \w* endpoint
# View for redirecting to a long_url at a custom or short url 
def shortened_url_view(request, short_url=''):
    if short_url == '':
        #TODO Make simple landing page
        shorts = Short_URL.objects.all()
        customs = Custom_URL.objects.all()
        template = loader.get_template('index.html')
        context = RequestContext(request, {
            'shorts': shorts,
            'customs': customs
        })
        return HttpResponse(template.render(context))
        
    else:
        long_url_list = Short_URL.objects.filter(short_url = short_url)
        custom_url_list = Custom_URL.objects.filter(custom_url = short_url)
        if len(long_url_list) + len(custom_url_list) == 0:
            return HttpResponse('This url is not yet shortened')
        # If shortened url exists redirect to long_url with html meta tag
        elif len(long_url_list) > 0:
            obj = long_url_list[0]
            obj.number_visits += 1
            obj.save()
        elif len(custom_url_list) > 0:
            obj = custom_url_list[0].short_url
            obj.number_visits += 1
            obj.save()
        return HttpResponse('<meta http-equiv="refresh" content="0; URL=\'' + obj.long_url + '\'" />)')


# makes random url string of length 6 
def makeShortURLString(banned_names = []):
    banned_names.append('')
    poss = '0123456789abcdefghijklmnopqrstuvwxyz'
    l = len(poss)
    s = ''
    for i in range(6):
        ri = random.randint(0, l - 1)
        s += poss[ri]
    # If short_url already exists (even as a custom url), make a new short_url, else, return s
    confirm = confirmAvailableURL(s)
    if confirm and (s not in banned_names):
        return s 
    return makeShortURLString(banned_names) 


# Checks if url is available as short url or custom url
def confirmAvailableURL(url):
    short_url_count = Short_URL.objects.filter(short_url = url).count()
    custom_url_count = Custom_URL.objects.filter(custom_url = url).count()
    if (short_url_count + custom_url_count) > 0:
        return False
    else:
        return True

# Makes new ShortURLObj TODO Move to models.py
def makeShortURLObj(long_url, banned_names=[]):
    short_url = makeShortURLString(banned_names=banned_names)
    tld = tldextract.extract(long_url)
    domain = tld.domain + '.' + tld.suffix
    number_visits = 0
    time_stamp = str(datetime.datetime.now())
    new_url_obj = Short_URL.objects.create(long_url=long_url, short_url=short_url, domain=domain, time_stamp=time_stamp, number_visits=number_visits)
    return new_url_obj
