# Generated by Django 3.2.7 on 2021-10-23 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detail', '0006_categoryclass_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='subfeature',
            name='name_banorte',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='subfeature',
            name='name_bbva',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='subfeature',
            name='name_santander',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='subfeature',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]
