# Generated by Django 3.1.7 on 2021-10-05 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0002_auto_20211005_1404'),
    ]

    operations = [
        migrations.RenameField(
            model_name='referral',
            old_name='status',
            new_name='paid_status',
        ),
        migrations.AddField(
            model_name='referral',
            name='request_status',
            field=models.BooleanField(default=False),
        ),
    ]
