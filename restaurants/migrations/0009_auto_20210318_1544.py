# Generated by Django 3.1.5 on 2021-03-18 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurants', '0008_itinerary_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='itinerary',
            name='cases',
            field=models.ManyToManyField(to='restaurants.Case'),
        ),
        migrations.AlterField(
            model_name='itinerary',
            name='user',
            field=models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.PROTECT, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]