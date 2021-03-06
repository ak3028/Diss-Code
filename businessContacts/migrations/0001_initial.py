# Generated by Django 3.2.5 on 2021-08-11 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('uploadBusinessCard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contactName', models.CharField(max_length=300)),
                ('contactOrganization', models.CharField(max_length=200)),
                ('contactEmail', models.EmailField(max_length=100)),
                ('contactPhoneNumber', models.CharField(max_length=20)),
                ('contactCardInfo', models.CharField(max_length=1000)),
                ('businessCard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uploadBusinessCard.businesscard')),
            ],
        ),
    ]
