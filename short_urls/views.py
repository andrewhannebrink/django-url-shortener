from django.shortcuts import render
from django.http import HttpResponse

def api_index(request):
   return HttpResponse('Welcome to my url shortener api')

def shortened_url_view(request):
   return HttpResponse('This url is not yet a shortened url')
