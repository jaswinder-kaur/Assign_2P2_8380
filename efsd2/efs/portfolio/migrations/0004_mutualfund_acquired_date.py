# Generated by Django 3.2.5 on 2021-07-11 18:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_mutualfund'),
    ]

    operations = [
        migrations.AddField(
            model_name='mutualfund',
            name='acquired_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]