import requests
from countrycode import countrycode
import json

r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address==thisdoesntwork&sensor=true&key=AIzaSyC61vF0pmAoVlia85hIhtUBx2G2hZkF1us')
response = json.loads(r.content)
results = response['results'][0]['formatted_address']
results = results.split()
print results
list_countries = []
country = results[len(results) - 1]
list_countries.append(country)
c_code = countrycode(codes = ['list_countries'], origin ='country_name', target = 'iso3c')
print c_code  
