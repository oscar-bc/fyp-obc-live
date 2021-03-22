from django.db import models
from attractions.models import Attraction
from django.contrib.auth.models import User


# Create your models here.
class Restaurant(models.Model):
    title = models.CharField(max_length=50)
    location = models.CharField(max_length=20)
    type_food = models.CharField(max_length=50)
    price = models.CharField(max_length=10)
    rating = models.FloatField()
    amount_reviews = models.IntegerField()
    review_link = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.title}"


class Case(models.Model):
    breakfast = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name='breakfast', db_column='breakfast')
    morning_activity = models.ForeignKey(Attraction, on_delete=models.PROTECT, related_name='morning_activity',
                                         db_column='morning_activity')
    lunch = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name='lunch', db_column='lunch')
    afternoon_activity = models.ForeignKey(Attraction, on_delete=models.PROTECT, related_name='afternoon_activity',
                                           db_column='afternoon_activity')
    dinner = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name='dinner', db_column='dinner')
    location = models.CharField(max_length=20)
    types_of_food = models.CharField(max_length=200, blank=True, null=True)
    price = models.CharField(max_length=10, blank=True, null=True)
    interests = models.CharField(max_length=200, blank=True, null=True)
    time_of_year = models.IntegerField(blank=True, null=True)
    type_of_holiday = models.CharField(max_length=20, blank=True, null=True)


class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user', db_column='user')
    cases = models.ManyToManyField(Case)
    saved = models.BooleanField()
    start_date = models.CharField(max_length=10, blank=True, null=True)
    end_date = models.CharField(max_length=10, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
