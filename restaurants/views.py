from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Restaurant
from .models import Case
from .models import Itinerary
from attractions.models import Attraction
from datetime import date, datetime
from .forms import UserSignupForm
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib import messages


# Create your views here.

def is_valid_queryparam(param):
    return param != '' and param is not None


def check(request):
    return render(request, 'restaurants/ask_save.html')


def home(request):
    return render(request, 'restaurants/home.html')


def profile(request):
    return render(request, 'restaurants/profile.html')


def itinerary(request):
    user_itinerary = Itinerary.objects.latest('id')
    user_itinerary.saved = True
    user_itinerary.save()
    message = "your itinerary has been saved"

    context = {
        'message': message
    }
    return render(request, 'restaurants/itinerary.html', context)


def error_message(request):
    return render(request, 'restaurants/error_message.html')


def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'username OR password is INCORRECT')
    context = {}
    return render(request, 'restaurants/login.html', context)


def userLogout(request):
    logout(request)
    return render(request, 'restaurants/logout.html')


def signup(request):
    userForm = UserSignupForm()

    if request.method == 'POST':
        userForm = UserSignupForm(request.POST)
        if userForm.is_valid():
            userForm.save()
            username = userForm.cleaned_data.get('username')
            password = userForm.cleaned_data.get('password1')

            user = authenticate(request, username=username, password=password)
            messages.success(request, 'User account created for: ' + username)
            auth_login(request, user)
            return redirect('/')
    context = {'form': userForm}
    return render(request, 'restaurants/signup.html', context)


def viewItineraries(request):
    user_itineraries = list(Itinerary.objects.filter(user=request.user, saved=True).values())

    context = {'itineraries': user_itineraries}
    return render(request, 'restaurants/view_itineraries.html', context)


def viewItinerary(request, itinerary_id):
    user_itinerary = Itinerary.objects.get(id=itinerary_id)
    cases = [val for val in user_itinerary.cases.all()]
    context = {'cases': cases,
               'itinerary': user_itinerary}
    return render(request, 'restaurants/view_itinerary.html', context)


def form(request):
    all_cases = Case.objects.all()
    restaurants = Restaurant.objects.all()
    attractions = Attraction.objects.all()
    location_query = request.GET.get('location')
    types_of_food_query = request.GET.getlist('type_food')
    price_query = request.GET.get('price')
    interests_query = request.GET.getlist('interests')
    start_date_query = request.GET.get('start_date')
    end_date_query = request.GET.get('end_date')
    type_holiday_query = request.GET.get('type_holiday')
    current_date = datetime.today().strftime('%Y-%m-%d')

    all_types_food = []
    all_types_attractions = []
    all_types_holidays = sorted(list({'Lads', 'Family', 'Cultural', 'Any', 'Romantic', 'Nature'}))

    enough_restaurants = True
    enough_attractions = True
    valid_form = True
    message = ""

    if location_query is "" or types_of_food_query is "" or interests_query is "" or start_date_query is "":
        valid_form = False

    type_holiday = "ANY"
    if type_holiday_query is not None:
        type_holiday = type_holiday_query.upper()

    for restaurant in restaurants:
        if " " in restaurant.type_food:
            types = restaurant.type_food.split(" ")
            for type in types:
                all_types_food.append(type)
        else:
            all_types_food.append(restaurant.type_food)
    all_unique_types_food = sorted(list(set(all_types_food)))
    all_unique_types_food.pop(0)

    for attraction in attractions:
        all_types_attractions.append(attraction.section)
    all_unique_types_attractions = sorted(list(set(all_types_attractions)))

    time_of_year = 0
    num_days = 1
    valid_date = True
    if is_valid_queryparam(start_date_query) and is_valid_queryparam(end_date_query):
        start_date_query = start_date_query.split("-")
        start_date = date(int(start_date_query[0]), int(start_date_query[1]), int(start_date_query[2]))
        end_date_query = end_date_query.split("-")
        end_date = date(int(end_date_query[0]), int(end_date_query[1]), int(end_date_query[2]))
        num_days = (end_date - start_date).days
        time_of_year = int(end_date_query[1])
        if end_date < start_date or num_days == 0:
            valid_date = False
    valid_restaurants = []
    valid_attractions = []

    if is_valid_queryparam(location_query):
        restaurants = restaurants.filter(location=location_query.upper())
        attractions = attractions.filter(location=location_query.upper())

    if is_valid_queryparam(price_query):
        restaurants = restaurants.filter(price=price_query.upper())
    if types_of_food_query is not None:
        for types in types_of_food_query:
            if is_valid_queryparam(types):
                if valid_restaurants is None:
                    valid_restaurants = list(restaurants.filter(type_food__icontains=types.upper()))
                else:
                    valid_restaurants += list(restaurants.filter(type_food__icontains=types.upper()))
    if interests_query is not None:
        for interest in interests_query:
            if is_valid_queryparam(interest):
                if valid_attractions is None:
                    valid_attractions = list(attractions.filter(section__icontains=interest.upper()))
                else:
                    valid_attractions += list(attractions.filter(section__icontains=interest.upper()))
    temp_valid_restaurants = []
    if valid_restaurants is not None:
        valid_restaurants.sort(key=lambda c: c.amount_reviews, reverse=True)
        temp_valid_restaurants = valid_restaurants

    temp_valid_attractions = []
    if valid_attractions is not None:
        valid_attractions.sort(key=lambda c: c.amount_reviews, reverse=True)
        temp_valid_attractions = valid_attractions
    similarity = 0
    valid_cases = []
    if types_of_food_query is not None and interests_query is not None and location_query is not None:
        for case in all_cases:
            similarity = 0
            if case.location == location_query.upper() and case.price == price_query.upper():
                if case.time_of_year is not None:
                    if time_of_year == case.time_of_year:
                        similarity += 2
                    elif time_of_year == case.time_of_year - 1 or time_of_year == case.time_of_year + 1:
                        similarity += 1
                    elif time_of_year == case.time_of_year - 2 or time_of_year == case.time_of_year + 2:
                        similarity += 0.5
                if case.type_of_holiday.upper() == type_holiday:
                    similarity += 2
                for food in types_of_food_query:
                    if food.upper() in case.types_of_food:
                        similarity += 2 / len(case.types_of_food.split(","))
                for interest in interests_query:
                    if interest.upper() in case.interests:
                        similarity += 2 / len(case.interests.split(","))
                if similarity == 8:
                    valid_cases.append(case)
                elif 4 < similarity < 8:
                    improved_case = case
                    time_difference = improved_case.time_of_year - time_of_year
                    breakfast = False
                    lunch = False
                    dinner = False
                    morning = False
                    afternoon = False
                    if -3 < time_difference < 3:
                        for food in types_of_food_query:
                            if food.upper() in improved_case.breakfast.type_food:
                                breakfast = True
                            if food.upper() in improved_case.lunch.type_food:
                                lunch = True
                            if food.upper() in improved_case.dinner.type_food:
                                dinner = True
                        for interest in interests_query:
                            if interest.upper() in case.morning_activity.section:
                                morning = True
                            if interest.upper() in case.afternoon_activity.section:
                                afternoon = True
                        if breakfast is not True:
                            improved_case.breakfast = valid_restaurants[0]
                            valid_restaurants.remove(valid_restaurants[0])
                        if lunch is not True:
                            improved_case.lunch = valid_restaurants[0]
                            valid_restaurants.remove(valid_restaurants[0])
                        if dinner is not True:
                            improved_case.dinner = valid_restaurants[0]
                            valid_restaurants.remove(valid_restaurants[0])
                        if morning is not True:
                            improved_case.morning_activity = valid_attractions[0]
                            valid_attractions.remove(valid_attractions[0])
                        if afternoon is not True:
                            improved_case.afternoon_activity = valid_attractions[0]
                            valid_attractions.remove(valid_attractions[0])
    if len(valid_restaurants) <= 3 and location_query is not None:
        enough_restaurants = False
    if len(valid_attractions) <= 2 and location_query is not None:
        enough_attractions = False
    cases = []
    temp_restaurant = None
    temp_attraction = None

    if valid_form is False:
        message = "Please fill out form correctly"
    else:
        if enough_restaurants is False:
            message += "Please add more restaurant types. "
        if valid_date is False:
            message += "Please insert valid dates. "
        if enough_attractions is False:
            message += "Please add more types of interests. "

    if location_query is not None and enough_restaurants is True and valid_date is True:
        for day in range(num_days):
            if len(valid_cases) is not 0:
                cases.append(valid_cases[0])
                valid_cases.pop(0)
            else:
                if valid_restaurants is None or len(valid_restaurants) <= 3:
                    valid_restaurants += temp_valid_restaurants
                if valid_attractions is None or len(valid_attractions) <= 2:
                    valid_attractions += temp_valid_attractions
                if valid_restaurants is not None and valid_attractions is not None:
                    while temp_restaurant is not None and len(valid_restaurants) >= 3 \
                            and valid_restaurants[0].title == temp_restaurant.title:
                        # print(len(valid_restaurants))
                        valid_restaurants.remove(valid_restaurants[0])
                    while len(valid_restaurants) >= 2 and valid_restaurants[0].title == valid_restaurants[1].title:
                        # print(len(valid_restaurants))
                        valid_restaurants.remove(valid_restaurants[1])
                    while len(valid_restaurants) >= 2 and valid_restaurants[1].title == valid_restaurants[2].title:
                        # print(len(valid_restaurants))
                        valid_restaurants.remove(valid_restaurants[2])
                    while temp_attraction is not None and len(valid_attractions) >= 2 \
                            and valid_attractions[0].title == temp_attraction.title:
                        # print(len(valid_attractions))
                        valid_attractions.remove(valid_attractions[0])
                    while len(valid_attractions) >= 2 and valid_attractions[0].title == valid_attractions[1].title:
                        # print(len(valid_attractions))
                        valid_attractions.remove(valid_attractions[1])

                    if valid_restaurants is None or len(valid_restaurants) <= 3:
                        valid_restaurants += temp_valid_restaurants
                    if valid_attractions is None or len(valid_attractions) <= 2:
                        valid_attractions += temp_valid_attractions

                    if valid_attractions[0].section == valid_attractions[1].section:
                        interests = valid_attractions[0].section
                    else:
                        interests = valid_attractions[0].section + ", " + valid_attractions[1].section

                    if valid_restaurants[0].type_food == valid_restaurants[1].type_food and valid_restaurants[
                        0].type_food == \
                            valid_restaurants[2].type_food:
                        types_of_food = valid_restaurants[0].type_food
                    elif valid_restaurants[0].type_food == valid_restaurants[1].type_food:
                        types_of_food = valid_restaurants[0].type_food + ", " + valid_restaurants[2].type_food
                    elif valid_restaurants[0].type_food == valid_restaurants[2].type_food:
                        types_of_food = valid_restaurants[1].type_food + ", " + valid_restaurants[2].type_food
                    elif valid_restaurants[1].type_food == valid_restaurants[2].type_food:
                        types_of_food = valid_restaurants[0].type_food + ", " + valid_restaurants[2].type_food
                    else:
                        types_of_food = valid_restaurants[0].type_food + ", " + valid_restaurants[1].type_food + ", " + \
                                        valid_restaurants[2].type_food
                    temp_restaurant = valid_restaurants[2]
                    temp_attraction = valid_attractions[1]
                    case = Case.objects.create(
                        breakfast=valid_restaurants[0],
                        morning_activity=valid_attractions[0],
                        lunch=valid_restaurants[1],
                        afternoon_activity=valid_attractions[1],
                        dinner=valid_restaurants[2],
                        location=valid_restaurants[2].location,
                        types_of_food=types_of_food,
                        price=valid_restaurants[2].price,
                        interests=interests,
                        time_of_year=time_of_year,
                        type_of_holiday=type_holiday,
                    )
                    valid_restaurants.remove(valid_restaurants[0])
                    valid_restaurants.remove(valid_restaurants[0])
                    valid_restaurants.remove(valid_restaurants[0])
                    valid_attractions.remove(valid_attractions[0])
                    valid_attractions.remove(valid_attractions[0])
                    cases.append(case)
        if request.user.username != "":
            start_date_string = ""
            end_date_string = ""
            for ele in start_date_query:
                start_date_string += ele + "/"
            for ele in end_date_query:
                end_date_string += ele + "/"
            user_itinerary = Itinerary.objects.create(
                user=request.user,
                saved=False,
                start_date=start_date_string[:-1],
                end_date=end_date_string[:-1],
                location=location_query
            )
            user_itinerary.save()
            for case in cases:
                user_itinerary.cases.add(case)
    context = {
        'cases': cases,
        'types_food': all_unique_types_food,
        'types_attractions': all_unique_types_attractions,
        'types_holidays': all_types_holidays,
        'message': message
    }
    if len(cases) != 0:
        return render(request, 'restaurants/itinerary.html', context)
    elif enough_restaurants is False or valid_form is False or enough_attractions is False or valid_date is False:
        return render(request, 'restaurants/form.html', context)
    else:
        return render(request, 'restaurants/form.html', context)
