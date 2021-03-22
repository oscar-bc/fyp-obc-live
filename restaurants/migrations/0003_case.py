# Generated by Django 3.1.5 on 2021-02-14 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0002_auto_20210131_1530'),
        ('restaurants', '0002_auto_20210131_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=20)),
                ('afternoon_activity', models.ForeignKey(db_column='afternoon_activity', on_delete=django.db.models.deletion.PROTECT, related_name='afternoon_activity', to='attractions.attraction')),
                ('breakfast', models.ForeignKey(db_column='breakfast', on_delete=django.db.models.deletion.PROTECT, related_name='breakfast', to='restaurants.restaurant')),
                ('dinner', models.ForeignKey(db_column='dinner', on_delete=django.db.models.deletion.PROTECT, related_name='dinner', to='restaurants.restaurant')),
                ('lunch', models.ForeignKey(db_column='lunch', on_delete=django.db.models.deletion.PROTECT, related_name='lunch', to='restaurants.restaurant')),
                ('morning_activity', models.ForeignKey(db_column='morning_activity', on_delete=django.db.models.deletion.PROTECT, related_name='morning_activity', to='attractions.attraction')),
            ],
        ),
    ]
