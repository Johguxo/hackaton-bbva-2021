
import logging

from django.contrib.auth.models import User
from profiles.models import UserData

from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.encoding import smart_str
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from rest_framework.authentication import SessionAuthentication
from oauthlib.common import generate_token
from django.conf import settings

logger_tokens = logging.getLogger('token_logger')

def create_username(first_name, last_name):
    """create username account
        parameters
        ----------
        first_name: String
            first name of user account
        last_name: String
            last name of user account"""
    first_name = first_name.split(" ")[0].replace(".", "")
    if len(last_name) > 0:
        last_name = last_name.split(" ")[0].replace(".", "")
        username = (first_name + "." + last_name).lower()
    else:
        username= (first_name + ".user").lower()
    usernames = User.objects.filter(username__contains=username).order_by('id')
    if usernames:
        for user_name in usernames:
            repeated_username = user_name.username
            first_part = repeated_username.split('.')[0]
            second_part = repeated_username.split('.')[1]
            if (username.split('.')[0] == first_part and
                    username.split('.')[1] == second_part):
                split_repeated_username = repeated_username.split('.')
                if len(split_repeated_username) == 2:
                    username = username + '.1'
                else:
                    count = int(repeated_username.split('.')[2])
                    count += 1
                    if len(split_repeated_username) == 3:
                        split_repeated_username[2] = str(count)
                        username = '.'.join(split_repeated_username)
                    else:
                        username = username + '.' + str(count)
    return username

def create_user(dict_post):
    """ Create a user """
    exists_user = User.objects.filter(email=dict_post['email']).exists()
    if not exists_user:
        dict_post['firstName'] = (dict_post['firstName']).title()
        if dict_post['lastName'] != 'null':
            dict_post['lastName'] = (dict_post['lastName']).title()
        else:
            dict_post['lastName'] = ''
        username = create_username(dict_post['firstName'],
                                   dict_post['lastName'])
        user = User.objects.create(username=username,
                                   email=dict_post['email'],
                                   password='',
                                   first_name=dict_post['firstName'],
                                   last_name=dict_post['lastName'])
        if 'password' in dict_post:
            if dict_post['password'] == '1234':
                password = 'PassWordBBVABackend'
            else:
                password = dict_post['password']
        else:
            password = User.objects.make_random_password()
        user.set_password(password)
        user.save()
        ###
        # REST addon
        ###
        userdata = UserData.objects.create(user=user,
                                           n_status=1)
        userdata.save()
        ###
        return user
    else:
        return None

def create_token(username, password, request, is_authenticated=False):
    """
    Function to create a token for a user.
    Returns a dictionary with tokens
    """
    if is_authenticated:
        """
        url = (protocol + request.META['HTTP_HOST'] +
               "/o/token/?grant_type=password&" + "client_id=" +
               app['client_id'].value + "&" + "client_secret=" +
               app['client_secret'].value + "&" + "username=" +
               username + "&" + "password=" + password + "&" + 
               "date=" + str(timezone.now()))
        request_content = requests.post(url)
        r_json = request_content.json()
        """
        user = User.objects.get(username=username)
        expires = (timezone.now() + 
                   timedelta(seconds=settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS']))
        access_token = AccessToken(token=generate_token(),
                                   expires=expires,
                                   user=user)
        access_token.save()
        refresh_token = RefreshToken(user=user,
                                     token=generate_token(),
                                     access_token=access_token
                                     )
        refresh_token.save()
        r_json = {'access_token': access_token.token,
                  'refresh_token': refresh_token.token}
        if 'access_token' not in r_json:
            try:
                logger_tokens.info(
                    'USERNAME: ' + username + '\n'
                )
            except:
                pass
                # Error log
    else:
        user = User.objects.get(username=username)
        expires = (timezone.now() + 
                   timedelta(seconds=settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS']))
        access_token = AccessToken(token=generate_token(),
                                   expires=expires,
                                   user=user)
        access_token.save()
        refresh_token = RefreshToken(user=user,
                                     token=generate_token(),
                                     access_token=access_token
                                     )
        refresh_token.save()
        r_json = {'access_token': access_token.token,
                  'refresh_token': refresh_token.token}
        if 'access_token' not in r_json:
            try:
                logger_tokens.info(
                    'USERNAME: ' + username + '\n'
                    + 'RESPONSE STATUS ' + str(200) + '\n'
                )
            except:
                pass
            # Error log
    rest_data = {'access_token': r_json['access_token'],
                 'refresh_token': r_json['refresh_token']}
    return rest_data

def parse_login_request_log(request_headers, request_items, response_items, user_not_authenticated, response_succesful):
    password_params_list = ['password', 'pass']
    http_method = request_headers['REQUEST_METHOD']
    headers_to_log = ['PATH_INFO', 'QUERY_STRING',
                      'REMOTE_HOST', 'HTTP_REFERER', 'HTTP_USER_AGENT']
    log_lines = [
        '### AUTH ATTEMPT -->',
        '# HEADERS:'
    ]
    log_lines.append('    - \'REQUEST_METHOD\': \'' + str(http_method) + '\'')
    for header in headers_to_log:
        if header in request_headers:
            log_lines.append('    - \'' + header +
                             '\': \'' + str(request_headers[header]) + '\'')
        else:
            log_lines.append('    - \'' + header +
                             '\': (UNDEFINED)')
    log_lines.append('# REQUEST:')
    for request_item in request_items:
        if str(request_item[0]) in password_params_list:
            log_lines.append('    - \'' +  str(request_item[0]) +
                             '\': (FORBIDDEN)')
        else:    
            log_lines.append('    - \'' +  str(request_item[0]) +
                             '\': \'' + smart_str(str(request_item[1]), encoding='utf-8') + '\'')
    log_lines.append('# RESPONSE:')
    for response_item in response_items:
        log_lines.append('    - \'' +  str(response_item[0]) +
                         '\': \'' + smart_str(str(response_item[1]), encoding='utf-8') + '\'')
    if user_not_authenticated:
        log_lines.append('# USER EXISTS?: NO')
    else:
        log_lines.append('# USER EXISTS?: YES')
    if response_succesful:
        log_lines.append('# SERVER RESPONSE: AUTH SUCCESFUL!')
    else:
        log_lines.append('# SERVER RESPONSE: AUTH FAILED!')
    log_str = '\n' + '\n'.join(log_lines) + '\n'
    return log_str