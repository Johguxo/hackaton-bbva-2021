from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils.translation import deactivate
from institution.models import Institution, UserInstitution
from resource.models import File, UserInstitutionFile
from datetime import datetime, timedelta
from django.utils import timezone
# Create your models here.

class TypeTransaction(models.Model): 
    TYPE = (
        (0, 'NO ASSIGN '),
        (1, 'POSITIVE'),
        (2, 'NEGATIVE')
    )
    name = models.IntegerField(default=0,blank=True, null=True)

    def __str__(self):
        return self.type.get_type_display()

class Transaction(models.Model):
    user_institution_file = models.ForeignKey(UserInstitutionFile,on_delete=models.CASCADE)
    type_transaction = models.ForeignKey(TypeTransaction,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    creation = models.DateField(default=timezone.now)

class Recomendation(models.Model):
    content = models.TextField(default='')
    #image = models.ImageField()
    creation = models.DateField(default=timezone.now)

class UserRecomendation(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    recomendation = models.ForeignKey(Recomendation, on_delete=CASCADE)
    initial_date = models.DateField(default=timezone.now)
    final_date = models.DateField(default=timezone.now)

class Category(models.Model):
    name = models.CharField(default='',max_length=150,null=True, blank=True)
    description = models.TextField(default='',null=True, blank=True)

    def __str__(self):
        if self.name:
            return (self.name)
        return 'No hay nombre'

class Report(models.Model):
    name = models.CharField(max_length=150,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=CASCADE,null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        if self.name:
            return (self.name)
        return 'No hay nombre'

class Season(models.Model):
    year = models.IntegerField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=150,null=True, blank=True)

    def __str__(self):
        return (str(self.year) +' - ' + 
        str(self.number) + ': ' + self.description)

class CategoryClass(models.Model):
    name = models.CharField(max_length=150,null=True, blank=True)
    status = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return (self.name + ': ' + str(self.priority))

class CategoryClassReport(models.Model):
    report = models.ForeignKey(Report, on_delete=CASCADE,null=True, blank=True)
    category_class = models.ForeignKey(CategoryClass, on_delete=CASCADE,null=True, blank=True)

    def __str__(self):
        return (self.report.name + '(' +str(self.category_class.priority)+ ')'+': ' + self.category_class.name)

class Feature(models.Model):
    name = models.CharField(max_length=150,null=True, blank=True)
    name_bbva = models.CharField(max_length=150,null=True, blank=True)
    name_banorte = models.CharField(max_length=150,null=True, blank=True)
    name_santander = models.CharField(max_length=150,null=True, blank=True)
    category_class = models.ForeignKey(CategoryClass,on_delete=CASCADE,null=True, blank=True)
    priority = models.IntegerField(default=0)
    have_sub_feature = models.BooleanField(default=False)
    is_total = models.BooleanField(default=False)
    is_subtotal = models.BooleanField(default=False)

    def __str__(self):
        valid_sub_features = '0'
        if self.have_sub_feature:
            valid_sub_features = '1'
        str_priority = "No designado"
        if self.priority:
            str_priority = str(self.priority)
        return (self.category_class.name + ' (' + str_priority + ') : ' + self.name + ' - sub_fea: ' + valid_sub_features)

class SubFeature(models.Model):
    name = models.CharField(max_length=150,null=True, blank=True)
    name_bbva = models.CharField(max_length=150,null=True, blank=True)
    name_banorte = models.CharField(max_length=150,null=True, blank=True)
    name_santander = models.CharField(max_length=150,null=True, blank=True)
    feature = models.ForeignKey(Feature, on_delete=CASCADE)
    priority = models.IntegerField(default=0)

    def __str__(self):
        str_priority = "No designado"
        if self.priority:
            str_priority = str(self.priority)
        return (self.feature.name + ' (' + str_priority + ') : ' + self.name)


class Detail(models.Model):
    TYPE = (
        (0, 'NO ASSIGN '),
        (1, 'POSITIVE'),
        (2, 'NEGATIVE')
    )
    amount = models.FloatField(default=0.0)
    type_movement = models.IntegerField(default=1)
    season = models.ForeignKey(Season,on_delete=CASCADE)
    bank = models.ForeignKey(Institution, on_delete=CASCADE,null=True, blank=True)
    have_sub_detail = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.season.description + ' - ' +self.bank.name + ' : '+str(self.amount)

class SubDetail(models.Model):
    CATEGORY_DETAIL = (
        (0, 'NO ASSIGN '),
        (1, 'Capital Contribuido'),
        (2, 'Capital Ganado')
    )
    title = models.CharField(max_length=150,null=True, blank=True)
    detail = models.ForeignKey(Detail,on_delete=CASCADE,null=True, blank=True)
    category_title = models.IntegerField(default=0,choices=CATEGORY_DETAIL)

class DetailFeature(models.Model):
    detail = models.ForeignKey(Detail,on_delete=CASCADE,null=True, blank=True)
    feature = models.ForeignKey(Feature, on_delete=CASCADE)

    def __str__(self):
        return self.feature.name + ' - ' +self.detail.bank.name + ' : '+str(self.detail.amount)

class DetailSubfeature(models.Model):
    detail = models.ForeignKey(Detail,on_delete=CASCADE,null=True, blank=True)
    subfeature = models.ForeignKey(SubFeature, on_delete=CASCADE)

    def __str__(self):
        return self.subfeature.name + ' - ' +self.detail.bank.name + ' : '+str(self.detail.amount)

class ReportInstitution(models.Model):
    report = models.ForeignKey(Report, on_delete=CASCADE,null=True, blank=True)
    institution = models.ForeignKey(Institution, on_delete=CASCADE)
    def __str__(self):
        if self.report.name:
            return (self.institution.name + ': ' + self.report.name)
        return 'No hay nombre'