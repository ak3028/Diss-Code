# Generated by Django 3.2.3 on 2021-06-17 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploadBusinessCard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name = 'businesscard',
            name = 'isProcessed',
            field = models.CharField(max_length=1, null=True),
        ),
        migrations.AddField(
            model_name = 'businesscard',
            name = 'submittedDate',
            field = models.DateField(null=True),
        ),
    ]
