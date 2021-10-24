import requests
import json
from datetime import datetime, timedelta
from detail.models import Category, Feature, Report, CategoryClass
from rest_framework.serializers import ModelSerializer, ReadOnlyField,\
                                       HyperlinkedModelSerializer
from rest_framework.fields import SerializerMethodField, DateTimeField
from oauth2_provider.models import AccessToken, Application, RefreshToken
from django.contrib.auth.models import User

from resource.models import UserInstitutionFile, File

class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class FeatureSerializer(ModelSerializer):

    class Meta:
        model = Feature
        fields = '__all__'


class ReportSerializer(ModelSerializer):
    
    class Meta:
        model = Report
        fields = '__all__'
