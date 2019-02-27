# Generated by Django 2.1.4 on 2019-02-26 12:30

from django.db import migrations, models
import django.db.models.deletion
from poll.management.commands.scrape_loksabha_constituencies import DATA_DIR, filename
import json


def populate_data(apps, schema_editor):
    jsonfile = DATA_DIR / filename.format("json")

    with open(jsonfile) as f:
        data = json.load(f)

        state_union_model = apps.get_model("poll", "StateUnion")
        constituency_model = apps.get_model("poll", "Constituency")

        for su, cons in data.items():
            su_obj = state_union_model.objects.create(name=su)
            for c in cons:
                constituency_model.objects.create(state_union=su_obj, name=c)


def unpopulate_data(apps, model_name):
    # using on delete cascade in constituency model which has StateUnion as foreignkey
    # so deleting StateUnion objects will delete Constituency objects too :)
    model = apps.get_model("poll", "StateUnion")
    model.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0002_auto_20190226_0226'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='StateUnion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='constituency',
            name='state_union',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.StateUnion'),
        ),
        migrations.RunPython(populate_data, reverse_code=unpopulate_data)
    ]