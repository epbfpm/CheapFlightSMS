import requests as r
from os import environ
from datetime import datetime as dt
from datetime import timedelta as td
import pandas
from url_shortener import *


results = ''
# ----- DATA -----
data = pandas.read_csv('Flight Deals - prices.csv').to_dict(orient='records')

# ----- TODAY -----
dateFrom = dt.now().strftime('%d/%m/%Y')
dateTo = (dt.now() + td(90)).strftime('%d/%m/%Y')

# ----- TEQUILA API COMMON VARIABLES -----
tequila_apikey = environ.get('tequila_apikey')
tequila_endpoint = 'http://api.tequila.kiwi.com'
headers = {'apikey': tequila_apikey}


# ----- SHEET DATA -----
def crawler(n):
    fly_to, fly_from, price_to = data[n]['City'], data[n]['IATA Code'], data[n]['Lowest Price']
    return fly_to, fly_from, str(price_to)


def iata_code(destination):
    ic_params = {
        'term': destination,
        'location_types': 'airport',
        'active_only': 'true',
    }
    iata = r.get(f'{tequila_endpoint}/locations/query', params=ic_params, headers=headers)
    iata = iata.json()['locations'][0]['id']
    return iata


def flight_search():
    global results
    for n in range(0, len(data)):
        fly_to, fly_from, price_to = crawler(n)
        fs_params = {'fly_from': fly_from,
                     'fly_to': iata_code(fly_to),
                     'dateFrom': dateFrom,
                     'dateTo': dateTo,
                     'nights_in_dst_from': 7,
                     'nights_in_dst_to': 28,
                     'flight_type': 'round',
                     'one_for_city': 1,
                     'max_stopovers': 2,
                     'curr': 'BRL',
                     'price_to': price_to,
                     }
        try:
            server = r.get(f'{tequila_endpoint}/v2/search', params=fs_params, headers=headers)
            server.raise_for_status()
            server = server.json()['data']
            price = server[0]['price']
            route = server[0]['route']
            city_from = route[0]['cityFrom']
            city_to = route[1]['cityFrom']
            airline = route[0]['airline']
            flight_number = route[0]['flight_no']
            from_date = route[0]['local_departure'].split('T')[0].split('-')
            from_date = f'{from_date[2]}/{from_date[1]}/{from_date[0]}'
            from_time = route[0]['local_departure'].split('T')[1].split('.')[0].split(':')
            from_time = f'{from_time[0]}:{from_time[0]}'
            to_date = route[1]['local_departure'].split('T')[0].split('-')
            to_date = f'{to_date[2]}/{to_date[1]}/{to_date[0]}'
            to_time = route[1]['local_departure'].split('T')[1].split('.')[0].split(':')
            to_time = f'{to_time[0]}:{to_time[0]}'
            url = short_url(server[0]['deep_link'])
            ticket_msg = f'{airline} {flight_number}. R$ {price},00! From: {city_from}({fly_from}), {from_date} {from_time} To: {city_to}({iata_code(fly_to)}), {to_date} {to_time}. Buy here: {url}\n\n'
            results = results + ticket_msg
            print(results)
        except IndexError:
            pass
    return results
