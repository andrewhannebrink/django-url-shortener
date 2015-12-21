from short_urls.models import Short_URL, Custom_URL
from rest_framework import serializers, viewsets

class Short_URL_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Short_URL
        fields = ('long_url','domain','short_url','number_visits','time_stamp')

class Short_URL_ViewSet(viewsets.ModelViewSet):
    queryset = Short_URL.objects.all()
    serializer_class = Short_URL_Serializer

class Custom_URL_Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Custom_URL
        fields = ('custom_url') #TODO add short url details

