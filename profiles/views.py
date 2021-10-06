import logging
from django.utils import timezone

from django.views import generic
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from profiles.models import FacebookUser, GoogleUser, UserData

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from oauth2_provider.models import Application, AccessToken
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from rest_framework.authentication import SessionAuthentication
from django.middleware.csrf import get_token

from profiles.utils import create_user, parse_login_request_log, create_token
from profiles.serializers import TokenSerializer

# Create your views here.
logger = logging.getLogger('login_logger')

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """ Class csrf exempt """

    def enforce_csrf(self, request):
        """ Redefinition of method """
        return  # To not perform the csrf check previously happening

class LandingPage(generic.View):
    template_name = 'profiles/landing_page.html'
    def get(self, request):
        dict_data = {}
        return TemplateResponse(
            self.request, self.template_name, dict_data
        )

class LoginPage(generic.View):
    template_name = 'profiles/login_page.html'
    def get(self, request):
        #dict_data = {}
        dict_data = {'access_token':get_token(request)}
        return TemplateResponse(
            self.request, self.template_name, dict_data
        )
    #return render(request,template_name)

class RegisterPage(generic.View):
    template_name = 'profiles/register_page.html'
    def get(self, request):
        #print(get_token(request))
        #dict_data = {'access_token': request.session['rest']['access_token']}
        dict_data = {'access_token':get_token(request)}
        return TemplateResponse(
            self.request, self.template_name, dict_data
        )

class LoginAPI(APIView):
    """ API used to login a user """
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self,request):
        context = {'request': request}
        response_error_dict = {'status': False, 'app': {'status': False}}
        if ('password' in self.request.data):
            user_query_params = {
                'is_active': True
            }
            if 'email' in self.request.data:
                if 'business' in self.request.data and 'instructor' in self.request.data:
                    user_query_params['email'] = request.data['email']
                else:
                    user_query_params['email'] = request.data['email']
            user = User.objects.filter(**user_query_params)
            is_authenticated = False
            password = request.data['password']
            if user.exists():
                obj_user = user.last()
                user = authenticate(
                        username=obj_user.username,
                        password=request.data['password']
                    )
                if user:
                    is_authenticated = True
                    login(request, user)
                else:
                    return Response(response_error_dict)
                rest = None
                tokens = AccessToken.objects.filter(
                    user=obj_user, expires__gt=timezone.now(),
                )
                if tokens.exists():
                    token = tokens.last()
                    rest = TokenSerializer(token, context=context).data
                else:
                    rest = create_token(
                        obj_user.username, password,
                        request, is_authenticated
                    )
                succesful_response = {
                    'rest': rest, 'user': user.get_full_name(),
                }
                return Response(succesful_response, status=status.HTTP_200_OK)

class RegisterAPI(APIView):
    """ API used to register a user """
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self,request):
        """ POST Method """
        dict_post = {}
        
        dict_post['firstName'] = ''
        dict_post['lastName'] = ''
        if 'firstname' in request.data:
            dict_post['firstName'] = request.data['firstname']
        if 'lastname' in request.data:
            dict_post['lastName'] = request.data['lastname']
        if 'email' in request.data:
            dict_post['email'] = request.data['email']
        dict_post['password'] = request.data['password']
        print(dict_post)
        new_user = create_user(dict_post)
        if new_user is not None:
            new_user_auth = authenticate(
                    username=new_user.username, 
                    password=dict_post['password']
            )
            if new_user_auth:
                is_authenticated = True
                login(request, new_user_auth)
                host = request.META['HTTP_HOST']
            else:
                response_dict = {'status': False, 'app': {'status': False}}
                try:
                    logger.info(
                        parse_login_request_log(
                            request.META,
                            request.query_params.items(),
                            response_dict.items(),
                            not new_user_auth,
                            False
                            )
                        )
                except:
                        print('Error login log')
                return Response(response_dict)
        return Response({'status':True})