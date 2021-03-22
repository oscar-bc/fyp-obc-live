from django.db import models


# Create your models here.
class Attraction(models.Model):
    type = models.CharField(max_length=15)
    title = models.CharField(max_length=50)
    location = models.CharField(max_length=20)
    section = models.CharField(max_length=50)
    rating = models.FloatField()
    amount_reviews = models.IntegerField()
    review_link = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.title}"
