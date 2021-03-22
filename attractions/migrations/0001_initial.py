# Generated by Django 3.1.5 on 2021-01-31 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=15)),
                ('title', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=20)),
                ('section', models.CharField(max_length=50)),
                ('rating', models.IntegerField()),
                ('amount_reviews', models.IntegerField()),
                ('review_link', models.CharField(max_length=300)),
            ],
        ),
    ]