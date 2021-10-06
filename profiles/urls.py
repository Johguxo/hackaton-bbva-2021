from django.conf.urls import url
from django.urls import include,path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()

urlpatterns = [
    url(r'^login/', views.LoginPage.as_view()),
    url(r'^register/', views.RegisterPage.as_view()),
    url(r'^login-api/', views.LoginAPI.as_view()),
    url(r'^register-api/', views.RegisterAPI.as_view()),
]