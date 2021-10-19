from django.contrib import admin
from .models import TypeTransaction, Transaction, Recomendation, UserRecomendation
# Register your models here.
admin.site.register(TypeTransaction)
admin.site.register(Transaction)
admin.site.register(Recomendation)
admin.site.register(UserRecomendation)