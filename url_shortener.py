import urllib
import requests


def short_url(url):
    key = '1a88fdb4264c972bfb6cf88fabf553423bee5'
    url = urllib.parse.quote(url)
    name = ''
    userDomain = '0'
    r = requests.get('http://cutt.ly/api/api.php?key={}&short={}&name={}&userDomain={}'.format(key, url, name, userDomain))
    try:
        return r.json()['url']['shortLink']
    except:
        return 'no url available'



# ---- previous data from sheety ----- stopped working - only 200 feches a month
# shitty_endpoint = 'https://api.sheety.co/521e8d566af8db591780f0a9bf30ea3a/flightDeals/prices'
#
# def sheet():
#     server = r.get(url=shitty_endpoint)
#     server.raise_for_status()
#     data = server.json()['prices']
#     return data

