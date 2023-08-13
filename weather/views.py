import requests
import geocoder
from django.shortcuts import HttpResponse, render
from datetime import datetime






# Data Collecting snippets------------
def get_current_city():
    g = geocoder.ip("me")
    if g.ok:
        return g.city
    else:
        return None


# Input date in the format 'YYYY-MM-DD'


days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def data_parse(cityies):


    r = requests.get(
        url=f"http://api.weatherapi.com/v1/forecast.json?key=33e8806c1c9c45eb9a3144152230808&q={cityies}&days=5&aqi=no&alerts=no"
    )

    # Getting day
    def get_day(input_date):
        date_part = input_date.split()[0]
        date_object = datetime.strptime(date_part, "%Y-%m-%d")
        day_of_week = date_object.weekday()
        return days[day_of_week]
    
    curr = {
        "location": r.json()["location"]["name"],
        "condition": r.json()["current"]["condition"]["text"],
        "icon": r.json()["current"]["condition"]["icon"],
        "temperature": r.json()["current"]["temp_c"],
        "wind_kph": r.json()["current"]["wind_kph"],
        "wind_kph": r.json()["current"]["wind_kph"],
        "precip_mm": r.json()["current"]["precip_mm"],
        "humidity": r.json()["current"]["humidity"],
        "Day": get_day(r.json()["current"]["last_updated"]),
    }

    def days_info(days):
        return {"day": get_day(r.json()["forecast"]["forecastday"][days]["date"]),
                "centi_gr": r.json()["forecast"]["forecastday"][days]["day"]["maxtemp_c"],
                "condition": r.json()["forecast"]["forecastday"][days]["day"]["condition"]["text"],
                "icon": r.json()["forecast"]["forecastday"][days]["day"]["condition"]["icon"],}
    
    

    forcast = {
        "day1": days_info(1),
        "day2": days_info(2),
        "day3": days_info(3),
        "day4": days_info(4),
    }
    global data
    data = {"curr": curr, "forecast": forcast, "today": datetime.today}

# Data Collecting snippets ends-----


def Home(request):
    

    try:
        city = get_current_city()
        data_parse(city)
        
    except:
        data_parse("london")
    
    if request.method == "POST":
        got_city = request.POST.get("city")
        data_parse(got_city)
        
        return render(request, "index.html", data)
    
    return render(request, "index.html", data)



    
    
    