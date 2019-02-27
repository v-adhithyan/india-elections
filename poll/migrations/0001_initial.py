# Generated by Django 2.1.4 on 2019-02-26 01:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OpinionPoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('choices', models.CharField(choices=[('c', 'UPA - Congress - DMK'), ('b', 'NDA - BJP - ADMK - PMK'), ('o', 'Others'), ('n', 'Nota')], max_length=1)),
                ('age', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(18)])),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=1)),
                ('ip_address', models.GenericIPAddressField()),
                ('added_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
