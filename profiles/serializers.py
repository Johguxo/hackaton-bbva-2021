import requests
import json
from datetime import datetime, timedelta
from rest_framework.serializers import ModelSerializer, ReadOnlyField,\
                                       HyperlinkedModelSerializer
from rest_framework.fields import SerializerMethodField, DateTimeField
from oauth2_provider.models import AccessToken, Application, RefreshToken
from django.contrib.auth.models import User

from profiles.models import UserData

class UserSerializer(ModelSerializer):
    """ Serializer for User Model """
    data = SerializerMethodField()

    class Meta:
        """ Meta class for user serializer """
        model = User
        fields = ('id', 'first_name', 'last_name', 'username',
                  'email', 'date_joined', 'data')
        extra_kwargs = {'password': {'read_only': True},
                        'id': {'read_only': True, 'required': False},
                        'username': {'read_only': True, 'required': False},
                        'data': {'read_only': True, 'required': False},
                        'date_joined': {'read_only': True, 'required': False}}

    def get_data(self, obj):
        data = ''
        user_data = UserData.objects.filter(user=obj)
        if user_data.exists():
            data = UserDataSerializer(user_data.last()).data
        return data

class UserDataSerializer(ModelSerializer):
    """ Serializer for User Data Model"""

    class Meta:
        """ Meta class for user data serializer """
        model = UserData
        fields = '__all__'

# TokenSerializer doesn't seem to be used
class TokenSerializer(HyperlinkedModelSerializer):
    """ Serializer for the token of an user """
    user = UserSerializer()
    access_token = SerializerMethodField()
    status = SerializerMethodField()
    client_id = ReadOnlyField(source="application.client_id")
    client_secret = ReadOnlyField(source="application.client_secret")
    refresh_token = SerializerMethodField()

    class Meta:
        """ Meta class for the token serializer """
        model = AccessToken
        fields = ['access_token', 'user', 'status', 'client_id', 'client_secret',
                  'refresh_token']

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data """
        queryset = queryset.select_related('user')
        return queryset

    def get_status(self, obj):
        """ This method only return a boolean variable """
        return True

    def get_access_token(self, obj):
        return obj.token

    def get_refresh_token(self, obj):
        return RefreshToken.objects.filter(access_token=obj).last().token

class ApplicationSerializer(ModelSerializer):
    """ Serializer for the client token """
    status = SerializerMethodField('bool')
    

    class Meta:
        """ Meta class for Application serializer """
        model = Application
        fields = ('client_id', 'client_secret', 'status',)

    def bool(self, obj):
        """ This method only return a boolean variable """
        return True