from django.db import models
from django.contrib.auth.models import User
from institution.models import Institution, UserInstitution
from datetime import datetime
# Create your models here.

class File(models.Model):
    creation = models.DateField(default=datetime.now())

class UserInstitutionFile(models.Model):
    user_institution = models.ForeignKey(UserInstitution,on_delete=models.CASCADE)
    file=models.ForeignKey(File,on_delete=models.CASCADE)

    def __str__(self):
        return self.user_institution.username