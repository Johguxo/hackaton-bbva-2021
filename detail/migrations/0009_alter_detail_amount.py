# Generated by Django 3.2.7 on 2021-10-24 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detail', '0008_auto_20211023_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='amount',
            field=models.FloatField(default=0.0),
        ),
    ]