# Generated by Django 3.1.5 on 2021-03-20 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0009_auto_20210318_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='itinerary',
            name='end_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='itinerary',
            name='start_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]