from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^api/last_hundred', views.last_hundred, name='last_hundred'),
  url(r'^api/make_short', views.make_short, name='make_short'),
  url(r'^api/domains', views.domains, name='domains'),
  url(r'^(?P<short_url>\w*)', views.shortened_url_view, name='shortened_url_view'),
]
