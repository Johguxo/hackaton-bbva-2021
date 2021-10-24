from django.db import models
from django.contrib.auth.models import User
from institution.models import Institution, UserInstitution
from datetime import datetime
from django.utils import timezone
# Create your models here.

class File(models.Model):
    name = models.CharField(default='',max_length=150)
    description = models.TextField(default='',blank=True, null=True)
    url_file = models.URLField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    season = models.IntegerField(blank=True, null=True)
    creation = models.DateField(default=timezone.now)

    def __str__(self):
        if self.name:
            return str(self.id) + ' : ' + self.name + ' - ' + self.url_file
        else:
            return 'No tiene nombre'

class UserInstitutionFile(models.Model):
    user_institution = models.ForeignKey(UserInstitution,on_delete=models.CASCADE)
    file = models.ForeignKey(File,on_delete=models.CASCADE)

    def __str__(self):
        return (self.user_institution.user.first_name +' - ' + 
        self.user_institution.institution.name + ' - ' + self.file.name)