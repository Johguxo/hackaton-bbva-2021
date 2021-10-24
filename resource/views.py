from django.db.models import query
from django.shortcuts import render
from django.contrib.auth.models import User
from institution.models import Institution, UserInstitution
from profiles.models import FacebookUser, GoogleUser, UserData
from resource.models import UserInstitutionFile
from resource.serializers import InstitutionSerializer, UserInstitutionFileSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from oauth2_provider.models import Application, AccessToken
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.viewsets import ModelViewSet

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """ Class csrf exempt """

    def enforce_csrf(self, request):
        """ Redefinition of method """
        return  # To not perform the csrf check previously happening

class InstitutionAPI(ModelViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = InstitutionSerializer
    lookup_field = 'id'

    def get_queryset(self):
       if 'id_bank' in self.request.GET:
            id_bank = self.request.GET['id_bank']
            institution = Institution.objects.filter(id=id_bank)
            return institution

class UserInstitutionFileAPI(ModelViewSet):
    """ API used to obtain files of an user """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserInstitutionFileSerializer
    lookup_field = 'id'

    def get_queryset(self):
        queryset = UserInstitutionFile.objects.all()
        if 'id_user' in self.request.GET:
            id_user = self.request.GET['id_user']
            user = User.objects.get(id=id_user)
            user_institution = UserInstitution.objects.filter(user=user)
            queryset = UserInstitutionFile.objects.filter(
                user_institution__in=user_institution
            )
            if 'id_bank' in self.request.GET:
                id_bank = self.request.GET['id_bank']
                institution = Institution.objects.get(id=id_bank)
                user_institution = user_institution.filter(institution=institution).last()
                queryset = UserInstitutionFile.objects.filter(user_institution=user_institution)
        return queryset