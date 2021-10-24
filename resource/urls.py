from django.conf.urls import url
from django.urls import include,path
from . import views

urlpatterns = [
    url(r'^user-institution-file-api/$', 
    views.UserInstitutionFileAPI.as_view({'get': 'list', 'post': 'create'}),
    name='user-institution-file-api'),
    url(r'^institution-api/$', 
    views.InstitutionAPI.as_view({'get': 'list', 'post': 'create'}),
    name='institution-api'),
]