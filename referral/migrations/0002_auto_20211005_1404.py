# Generated by Django 3.1.7 on 2021-10-05 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]