from django.conf.urls import url
from django.urls import include,path
from . import views

urlpatterns = [
    url(r'^save-report-data-file-api/$', 
    views.SaveReportData.as_view(),
    name='report-data-file-api'),
    url(r'^category-api/$', 
    views.CategoryAPI.as_view({'get':'list'}),
    name='category-api'),
    url(r'^feature-api/$', 
    views.FeatureAPI.as_view({'get':'list'}),
    name='feature-api'),
    url(r'^data-report-api/$', 
    views.DataReportAPI.as_view(),
    name='data-report-api'),
    url(r'^details-data-api/$', 
    views.DataDetailsAPI.as_view(),
    name='data-details-report-api'),
]