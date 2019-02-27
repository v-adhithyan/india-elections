from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_tweetstats_comment_words'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alliance',
            name='party',
            field=models.CharField(choices=[('u', 'upa'), ('n', 'nda'), ('a', 'admk'), ('d', 'dmk')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='tweetstats',
            name='party',
            field=models.CharField(choices=[('u', 'upa'), ('n', 'nda'), ('a', 'admk'), ('d', 'dmk')], default='', max_length=1),
        ),
    ]
