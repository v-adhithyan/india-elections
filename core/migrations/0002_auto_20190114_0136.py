# Generated by Django 2.1.4 on 2019-01-14 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetstats',
            name='negative',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tweetstats',
            name='neutral',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tweetstats',
            name='positive',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
