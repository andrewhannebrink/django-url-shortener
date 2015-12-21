from django.shortcuts import render
from django.http import HttpResponse

def last_hundred(request):
   return HttpResponse('This is the api/last_hundred endpoint')

def shortened_url_view(request):
   return HttpResponse('This url is not yet a shortened url')

def make_short(request):
   return HttpResponse('This is the api/make_short endpoint')
