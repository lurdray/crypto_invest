# Generated by Django 3.1.7 on 2021-08-23 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.FileField(blank=True, default='default_files/default_face.png', upload_to='account_files/profile_photos/')),
                ('full_name', models.CharField(default='none', max_length=500)),
                ('other_name', models.CharField(default='none', max_length=500, null=True)),
                ('last_name', models.CharField(default='none', max_length=500, null=True)),
                ('house_address', models.TextField(default='none', null=True)),
                ('dob', models.CharField(default='none', max_length=500, null=True)),
                ('age', models.IntegerField(default=0)),
                ('id_image', models.FileField(blank=True, default='default_files/default_face.png', upload_to='account_files/id_images/')),
                ('id_number', models.CharField(default='none', max_length=500)),
                ('state_of_origin', models.CharField(default='none', max_length=500)),
                ('country', models.CharField(default='none', max_length=500)),
                ('language', models.CharField(default='none', max_length=500)),
                ('phone_no', models.CharField(default='none', max_length=500, null=True)),
                ('bank_name', models.CharField(default='none', max_length=500)),
                ('bank_verification_number', models.CharField(default='none', max_length=500, null=True)),
                ('bank_account_number', models.CharField(default='none', max_length=500)),
                ('bank_account_name', models.CharField(default='none', max_length=500)),
                ('payment_wallet_address', models.CharField(default='none', max_length=500)),
                ('public_key', models.CharField(default='none', max_length=500)),
                ('private_key', models.CharField(default='none', max_length=500)),
                ('status', models.BooleanField(default=False)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_type', models.CharField(default='none', max_length=500)),
                ('amount', models.CharField(default='none', max_length=500)),
                ('paid_status', models.BooleanField(default=False)),
                ('pfc_status', models.BooleanField(default=False)),
                ('proof_photo1', models.FileField(blank=True, default='default_files/default.png', upload_to='app_files/proof_photos/')),
                ('proof_photo2', models.FileField(blank=True, default='default_files/default.png', upload_to='app_files/proof_photos/')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('app_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_user.appuser')),
            ],
        ),
    ]