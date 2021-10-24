from django.db.models import query
from django.shortcuts import render
from django.contrib.auth.models import User
from numpy.lib.function_base import append
from detail.models import Category, CategoryClass, CategoryClassReport, Detail, DetailFeature, DetailSubfeature, Feature, Report, Season, SubFeature
from detail.serializers import CategorySerializer, FeatureSerializer, ReportSerializer
from detail.utils import create_detail_feature, create_detail_subfeature, extract_data, sacar_balance_banorte, sacar_balance_bbva, sacar_balance_santander
from institution.models import Institution, UserInstitution
from profiles.models import FacebookUser, GoogleUser, UserData
from resource.models import File, UserInstitutionFile
from resource.serializers import InstitutionSerializer, UserInstitutionFileSerializer
from django.db.models import Q
import math

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

class CategoryAPI(ModelViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def get_queryset(self):
        categories = Category.objects.all()
        return categories

class FeatureAPI(ModelViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FeatureSerializer
    lookup_field = 'id'

    def get_queryset(self):
        if 'id_category_class' in self.request.GET:
            features = Feature.objects.objects(category_class=self.request.GET['id_category_class'])
            return features

class ReportAPI(ModelViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReportSerializer
    lookup_field = 'id'

    def get_queryset(self):
        if 'id_report' in self.request.GET:
            reports = Report.objects.filter(id=self.request.GET['id_report'])
            return reports

class DataDetailsAPI(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if 'id_report' in self.request.GET:
            id_report = self.request.GET['id_report']
            report = Report.objects.filter(id=id_report)
            if report.exists():
                report = report.last()
                category_classes_report = CategoryClassReport.objects.filter(report=report)
                list_category_classes = []
                list_seasons = []
                for c_class_report in category_classes_report:
                    category_class = CategoryClass.objects.get(id=c_class_report.category_class.id)
                    features = Feature.objects.filter(category_class=category_class).order_by('priority')
                    list_response = []
                    for feature in features:
                        #print(feature.name)
                        details_feature = DetailFeature.objects.filter(feature=feature)
                        #print("C: ", details_feature.count())
                        list_amounts = []
                        if 'id_season' in self.request.GET:
                            season = Season.objects.get(id=self.request.GET['id_season'])
                            list_seasons = []
                            list_seasons.append({'name':season.description,'year':season.year,'number':season.number})
                            details_feature = details_feature.filter(detail__season=season)
                            if 'id_bank' in self.request.GET:
                                bank = Institution.objects.get(id=self.request.GET['id_bank'])
                                details_feature.filter(detail__bank=bank)
                            if details_feature.exists():
                                detail_feature = details_feature.last()
                                list_subfeatures = []
                                if feature.have_sub_feature:
                                    sub_features = SubFeature.objects.filter(feature=feature)
                                    for sub_feature in sub_features:
                                        detail_sub = DetailSubfeature.objects.filter(subfeature=sub_feature,detail__season=season,detail__bank=bank)
                                        if detail_sub.exists():
                                            detail_sub = detail_sub.last()
                                            if detail_sub.detail:
                                                list_subfeatures.append({'name':sub_feature.name,'amount':detail_sub.detail.amount})
                                list_response.append({'name': feature.name,
                                                        'amount':detail_feature.detail.amount,
                                                        'sub_features':list_subfeatures})
                        else:
                            seasons = Season.objects.all()
                            if 'id_bank' in self.request.GET:
                                bank = Institution.objects.get(id=self.request.GET['id_bank'])
                                details_feature = details_feature.filter(detail__bank=bank)
                                if self.request.GET['id_bank'] == '1':
                                    seasons = Season.objects.all().exclude(id=1)
                            list_subfeatures = []
                            if feature.have_sub_feature:
                                sub_features = SubFeature.objects.filter(feature=feature)
                                for sub_feature in sub_features:
                                    print(sub_feature.name)
                                    list_amounts_sub = []
                                    for season in seasons:
                                        detail_sub = DetailSubfeature.objects.filter(subfeature=sub_feature,
                                                                                    detail__season=season,
                                                                                    detail__bank=bank)
                                        for detail_item in detail_sub:
                                            list_amounts_sub.append(detail_item.detail.amount)
                                        print(list_amounts_sub)
                                    list_subfeatures.append({'name':sub_feature.name,'amount':list_amounts_sub})
                                    print("----")
                            list_seasons = []
                            for season in seasons:
                                list_seasons.append({'name':season.description,'year':season.year,'number':season.number})
                                if details_feature.filter(detail__season=season).exists():
                                    #print(list_seasons)
                                    detail_feature = details_feature.filter(detail__season=season).last()
                                    list_amounts.append(detail_feature.detail.amount)
                            """list_seasons = []
                            for season in seasons:
                                list_seasons.append({'name':season.description,'year':season.year,'number':season.number})
                                if details_feature.filter(detail__season=season).exists():
                                    #print(list_seasons)
                                    detail_feature = details_feature.filter(detail__season=season).last()
                                    list_amounts.append(detail_feature.detail.amount)
                                    list_subfeatures = []
                                    if feature.have_sub_feature:
                                        sub_features = SubFeature.objects.filter(feature=feature)
                                        for sub_feature in sub_features:
                                            list_amounts_sub = []
                                            detail_sub = DetailSubfeature.objects.filter(subfeature=sub_feature,
                                                                                        detail__season=season,
                                                                                        detail__bank=bank)
                                            print(sub_feature.name)
                                            for detail_item in detail_sub:
                                                print(season.description, detail_item.detail.amount)
                                                list_amounts_sub.append(detail_item.detail.amount)
                                            list_subfeatures.append({'name':sub_feature.name,'amount':list_amounts_sub})"""
                            list_response.append({'name': feature.name,
                                                'amount':list_amounts,
                                                'is_subtotal': feature.is_subtotal,
                                                'sub_features':list_subfeatures})
                    list_category_classes.append({'name':category_class.name,'features':list_response})
                    
                data_result = {'seasons':list_seasons,
                                'categories':list_category_classes}
                return Response({'status':True,'results':data_result})

        
class DataReportAPI(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if 'id_report' in self.request.GET:
            id_report = self.request.GET['id_report']
            report = Report.objects.filter(id=id_report)
            if report.exists():
                report = report.last()
                category_classes_report = CategoryClassReport.objects.filter(report=report)
                list_category_classes = []
                for c_class_report in category_classes_report:
                    category_class = CategoryClass.objects.get(id=c_class_report.category_class.id)
                    features = Feature.objects.filter(category_class=category_class)
                    list_features = []
                    for feature in features:
                        list_subfeatures = []
                        if feature.have_sub_feature:
                            sub_features = SubFeature.objects.filter(feature=feature)
                            for sub_feature in sub_features:
                                list_subfeatures.append({'name':sub_feature.name,
                                                        'priority':sub_feature.priority})
                        list_features.append({'name':feature.name,
                                                'priority':feature.id,
                                                'sub_features':list_subfeatures})
                    list_category_classes.append( {'priority':category_class.priority,
                                                'name': category_class.name,
                                                'features':list_features})
                return Response({'status':True,'results':list_category_classes})

class SaveReportData(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        if 'id_bank' in self.request.GET:
            bank = Institution.objects.get(id=self.request.GET['id_bank'])
            user_inst_file_q = UserInstitutionFile.objects.filter(user_institution__institution=bank)
            if 'id_report' in self.request.GET:
                id_report = request.GET['id_report']
                report = Report.objects.get(id=id_report)
                print("Generate report to: ", report.name + '(' + str(report.id) + ')' + ': ' + bank.name)
                category_class_report = CategoryClassReport.objects.filter(report=report)
                id_category_classes = list(category_class_report.values_list('id',flat=True))
                if self.request.GET['id_bank'] == '1':
                    data = sacar_balance_bbva(report.description)
                if self.request.GET['id_bank'] == '2':
                    data = sacar_balance_banorte(report.description)
                if self.request.GET['id_bank'] == '3':
                    data = sacar_balance_santander(report.description)
                list_features = (list(data[data.keys()[0]]))
                list_new = []
                for i in list_features :
                    if type(i) != type('str'):
                        if not math.isnan(i):
                            list_new.append(i.lower())
                        else:
                            list_new.append('')
                    else:
                        list_new.append(i.lower())
                list_features = list_new

                #list_features = [i.lower() for i in list_features if not i.isnan() ]
                #a,b = 'áéíóúüñÁÉÍÓÚÜÑ','aeiouunAEIOUUN'
                #trans = str.maketrans(a,b)
                #list_features = [i.translate(trans) for i in list_features]

                for index, name_feature in enumerate(list_features):
                    #print("Buscar:",name_feature)
                    if self.request.GET['id_bank'] == '1':
                        feature_q = Feature.objects.filter(
                            name_bbva__iexact=name_feature,
                            category_class_id__in=id_category_classes)
                        subfeature_q = SubFeature.objects.filter(
                            name_bbva__iexact=name_feature,
                            feature__category_class_id__in=id_category_classes)
                    if self.request.GET['id_bank'] == '2':
                        feature_q = Feature.objects.filter(
                            name_banorte__iexact=name_feature,
                            category_class_id__in=id_category_classes)
                        subfeature_q = SubFeature.objects.filter(
                            name_banorte__iexact=name_feature,
                            feature__category_class_id__in=id_category_classes)
                    if self.request.GET['id_bank'] == '3':
                        feature_q = Feature.objects.filter(
                            name_santander__iexact=name_feature,
                            category_class_id__in=id_category_classes)
                        subfeature_q = SubFeature.objects.filter(
                            name_santander__iexact=name_feature,
                            feature__category_class_id__in=id_category_classes)
                    last_feature = 'NINGUNA'
                    last_sub_feature = 'NINGUNA'
                    if feature_q.exists():
                        print("-----------Feature: ")
                        last_feature = feature_q.last()
                        data_amounts =  data.iloc[index,1:]
                        print(name_feature)
                        create_detail_feature(last_feature, data_amounts,int(self.request.GET['id_bank']))

                    if subfeature_q.exists():
                        print("-----SubFeature: ")
                        last_sub_feature = subfeature_q.last()
                        data_amounts =  data.iloc[index,1:]
                        print(name_feature)
                        create_detail_subfeature(last_sub_feature, data_amounts,int(self.request.GET['id_bank']))
                return Response({'status':True,'message':'Data guardada exitosamente'})
                #detail = Detail.objects.create(amount=amount_decimal,
                #                                season=season,
                #                                have_extra_info=True,
                #                                extra_info=dict_result)
        if 'id_file' in self.request.GET:
            file = File.objects.get(id=self.request.GET['id_file'])
            if 'id_report' in self.request.GET:
                id_report = request.GET['id_report']
                report = Report.objects.get(id=id_report)
                print("Generate report to: ", report.name + '(' + str(report.id) + ')')
                #data = obtain_data(file.url_file, type)
                user_inst_file_q = UserInstitutionFile.objects.filter(file=file)
                if user_inst_file_q.exists():
                    user_inst_file = user_inst_file_q.last()
                    year = file.year
                    number_season = file.season
                    if Season.objects.filter(year=year,number=number_season).exists():
                        season = Season.objects.filter(year=year,number=number_season).last()
                    institution_id = user_inst_file.user_institution.institution.id
                    data = extract_data(institution_id,report,file.url_file)
                    """if data['status']:
                        if data['is_have_dict']:
                            print("asda")
                    else:
                        return Response({'status': False, 'message':'Problema al extraer datos'})
                    if type == 1:
                        detail = Detail.objects.create(amount=0,season=season)
                    elif type == 5:
                        #Filas y Columnas
                        dict_result = '{Feature:0}'
                        detail = Detail.objects.create(amount=0,
                                                        season=season,
                                                        have_extra_info=True,
                                                        extra_info=dict_result)"""
                    return Response({'status':True,'message':'Data guardada exitosamente'})
        return Response({'status': False, 'message':'No existe tipo'})
