from django.contrib import admin
from .models import Restaurant
from .models import Case
from .models import Itinerary
# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Case)
admin.site.register(Itinerary)