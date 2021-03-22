from django.shortcuts import render
from .forms import CsvModelForm
from .models import Csv
import csv
from restaurants.models import Restaurant
from attractions.models import Attraction
#from django.http import HttpResponse


# Create your views here.
def add_attractions(row):
    if len(row[4]) > 1:
        row[4] = float(row[4])/10
    #print(row[4])
    type = row[0].upper()
    title = row[1].upper()
    location = row[2].upper()
    section = row[3].upper()
    rating = row[4]
    amount_reviews = row[5]
    review_link = row[6]
    Attraction.objects.create(
        type=type,
        title=title,
        location=location,
        section=section,
        rating=float(rating),
        amount_reviews=int(amount_reviews),
        review_link=review_link,
    )

def add_restaurants(row):
    if len(row[4]) > 1:
        row[4] = float(row[4])/10
    #print(row[4])
    title = row[0].upper()
    location = row[1].upper()
    type_food = row[2].upper()
    price = row[3].upper()
    rating = row[4]
    amount_reviews = row[5]
    review_link = row[6]
    Restaurant.objects.create(
        title=title,
        location=location,
        type_food=type_food,
        price=price,
        rating=float(rating),
        amount_reviews=int(amount_reviews),
        review_link=review_link,
    )

def upload_file_view(request):
    form = CsvModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvModelForm()
        obj = Csv.objects.get(activated=False)
        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f)

            for i, row in enumerate(reader):
                if i ==0:
                    pass
                else:
                    row = "".join(row)
                    row = row.replace("['", "")
                    row = row.split(";")
                    print(row)
                    if len(row[4]) > 1:
                        row[4] = float(row[4]) / 10
                    # print(row[4])
                    title = row[0].upper()
                    location = row[1].upper()
                    type_food = row[2].upper()
                    price = row[3].upper()
                    rating = row[4]
                    amount_reviews = row[5]
                    review_link = row[6]
                    Restaurant.objects.create(
                        title=title,
                        location=location,
                        type_food=type_food,
                        price=price,
                        rating=float(rating),
                        amount_reviews=int(amount_reviews),
                        review_link=review_link,
                    )
            obj.activated = True
            obj.save()
    return render(request, 'csvs/upload.html', {'form': form})
