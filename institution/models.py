from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
# Create your models here.

class Institution(models.Model):
    name = models.CharField(default='', max_length=250, blank=True, null=True)
    full_name = models.TextField(default='')
    n_status = models.IntegerField(default=1)
    date_creation = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

class UserInstitution(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE)
    n_status = models.IntegerField(default=1)

    def __str__(self):
        return self.user.first_name + '-' + self.institution.name
