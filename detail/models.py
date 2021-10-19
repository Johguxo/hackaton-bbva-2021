from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from institution.models import Institution, UserInstitution
from resource.models import File, UserInstitutionFile
from datetime import datetime, timedelta
# Create your models here.

class TypeTransaction(models.Model): 
    TYPE = (
        (1, 'POSITIVE'),
        (2, 'NEGATIVE')
    )
    name = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.type.get_type_display()

class Transaction(models.Model):
    user_institution_file = models.ForeignKey(UserInstitutionFile,on_delete=models.CASCADE)
    type_transaction = models.ForeignKey(TypeTransaction,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    creation = models.DateField(default=datetime.now)

class Recomendation(models.Model):
    content = models.TextField(default='')
    #image = models.ImageField()
    creation = models.DateField(default=datetime.now)

class UserRecomendation(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    recomendation = models.ForeignKey(Recomendation, on_delete=CASCADE)
    initial_date = models.DateField(default=datetime.now)
    final_date = models.DateField(default=datetime.now)






