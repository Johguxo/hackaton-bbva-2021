from django.contrib import admin
from .models import Category, CategoryClass, CategoryClassReport, Detail, DetailFeature, DetailSubfeature, Feature, Report, ReportInstitution, Season, SubFeature, TypeTransaction, Transaction, Recomendation, UserRecomendation
# Register your models here.
admin.site.register(TypeTransaction)
admin.site.register(Transaction)
admin.site.register(Recomendation)
admin.site.register(UserRecomendation)
admin.site.register(Category)
admin.site.register(Report)
admin.site.register(Season)
admin.site.register(Detail)
admin.site.register(Feature)
admin.site.register(SubFeature)
admin.site.register(CategoryClass)
admin.site.register(CategoryClassReport)
admin.site.register(DetailFeature)
admin.site.register(DetailSubfeature)
admin.site.register(ReportInstitution)
