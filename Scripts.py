
from requests_html import HTMLSession
import re
import random


def restaurant_roulette(input_city):
    session = HTMLSession()
    url = City_Grabber(input_city)
    print(url)
    r = session.get(url)
    html = r.html
    if r.status_code != 200:
        return "Some error occurred..."
    test_if_works = "#__next > div > div > div.ccl-d523c73794f30c03.ccl-917a4d5b8cd3a9e3.ccl-71fbf9dc5f85ebd4 > div > div.HomeLayout-b45e85df675abd0e > div > ul > li > span > div > div > h3"
    is_it_there = html.find(test_if_works)
    if is_it_there != []:
        return "Not available for this region. "
    path = '#__next > div > div > div.ccl-d523c73794f30c03.ccl-917a4d5b8cd3a9e3.ccl-71fbf9dc5f85ebd4 > div > div.HomeLayout-b45e85df675abd0e > div > ul > li > div > div > a'
    Restaurants = []
    Loop_over = r.html.find(path)
    for item in Loop_over:
        Restaurants.append(item.attrs["aria-label"])
    Restaurant_info = []
    for item in Restaurants:
        resto_name = re.split("(Bezorgt)",item)[0]
        Delivery_time = re.findall("Bezorgt[^B.]*",item)
        if Delivery_time == []:
            Delivery_time = ["Not given"]
        What = re.findall("Serveert.*",item)
        if What == []:
            What == ["Not Available"]
        Restaurant_info.append([resto_name,Delivery_time,What])
    return Restaurant_info

def City_Grabber(input_city):
    session = HTMLSession()
    url = "https://google.be/search?q=deliveroo+" + input_city
    r = session.get(url)
    html = r.html
    for item in html.find("#search"):
        link = item.find(".g")
        for item in link:
            link_of_item = item.find("a")[0].attrs["href"]
            if re.findall("deliveroo.be/nl-be/restaurants",link_of_item) != []:
                return link_of_item
        #first_link = link.find("a")[0].attrs["href"]
        #first_link = re.sub(".be/.*/rest",".be/nl-be/rest", first_link)
            continue
    
def Random_restaurant(input_city, digit=1, is_open = "False"):
    if is_open == "False":
        result = Check_if_open(input_city)
    else:
        result = restaurant_roulette(input_city)
    randint = random.randint(0,len(result))
    return result[randint][0]

def Check_if_open(input_city):
    open_restaurants = []
    results = restaurant_roulette(input_city)
    for item in results:
        if re.findall("minuten",item[1][0]) == []:
            continue
        else:
            open_restaurants.append(item)
    return open_restaurants

