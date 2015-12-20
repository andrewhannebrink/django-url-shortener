from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^api/', views.api_index, name='api_index'),
  url(r'^\w+', views.shortened_url_view, name='shortened_url_view'),
]
