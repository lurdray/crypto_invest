# Generated by Django 3.1.7 on 2021-10-03 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='message',
            field=models.TextField(default='none'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.CharField(default='none', max_length=500),
        ),
    ]
