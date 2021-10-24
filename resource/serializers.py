import requests
import json
from datetime import datetime, timedelta
from institution.models import Institution, UserInstitution
from rest_framework.serializers import ModelSerializer, ReadOnlyField,\
                                       HyperlinkedModelSerializer
from rest_framework.fields import SerializerMethodField, DateTimeField
from oauth2_provider.models import AccessToken, Application, RefreshToken
from django.contrib.auth.models import User

from resource.models import UserInstitutionFile, File

class InstitutionSerializer(ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'


class UserInstitutionSerializer(ModelSerializer):
    data_institution = SerializerMethodField()

    class Meta:
        model = UserInstitution
        fields = ('data_institution','id')

    def get_data_institution(self, obj):
        return InstitutionSerializer(obj.institution).data


class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class UserInstitutionFileSerializer(ModelSerializer):
    """ Serializer for file """
    data_user_institution = SerializerMethodField()
    data_file = SerializerMethodField()

    class Meta:
        """ Meta class for Application serializer """
        model = UserInstitutionFile
        fields = ('data_user_institution', 'data_file')
    
    def get_data_file(self,obj):
        data_file = FileSerializer(obj.file).data
        return data_file
    
    def get_data_user_institution(self, obj):
        data_user_institution = UserInstitutionSerializer(obj.user_institution).data
        return data_user_institution