import time
import tweepy
import json
import collections
import requests
from countrycode import countrycode
import json

start_time = time.time()

ckey = 'Ro4gqwM18nfFFkdtFHxHqg'
csecret = '6TsVTeYhMGsr5tw0i1GgwKC51xsCE2qELIsTAj5Vc'
atoken = '2383753860-nUOogjB0kAnH5DtXgMKYr0zWmC7V4MAlZ7qx44z'
asecret = '0N2y5corFRSSN1asTiEQgbtWBRDIL7CD365HkMqCmgf25'
s_name = "Angela_Merkel"

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)

ids = []
users = []
timezones = []
x = 0
for page in tweepy.Cursor(api.followers_ids, screen_name=s_name).pages():
    print('On page index %d' %x)
    x = x + 1
    user_ids = []
    for i in range(0, len(page), 100):
        user_ids.append(page[i:i+100])
    for i in user_ids:
        users.extend(api.lookup_users(i))
        time.sleep(4)
    #time.sleep(60)



print('Finished data collection. Starting to grab locations')

for item in users:
    timezones.append(item.time_zone)


print('There are %d timezones' %len(timezones))
#for thing in timezones:
#    print thing

country_hash = {}
print('Counting repeat data')
cnt = collections.Counter(timezones)
#print cnt
for key in cnt.keys():
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=='+ str(key) + '&sensor=true&key=AIzaSyC61vF0pmAoVlia85hIhtUBx2G2hZkF1us')
    response = json.loads(r.content)
    results = response['results']
    if(len(results) != 0):
        results = response['results'][0]['formatted_address']
        results = results.split()
        list_countries = []
        country = results[len(results) - 1]
        list_countries.append(country)
        c_code = countrycode(codes = list_countries, origin ='country_name', target = 'iso3c')
        if c_code[0] in country_hash.keys():
            country_hash[c_code[0]]['numberOfThings'] = country_hash[c_code[0]]['numberOfThings'] + cnt[key]
        else:
            country_hash[c_code[0]] = {}
            country_hash[c_code[0]]['numberOfThings'] = cnt[key]

max_things = 0
for key in country_hash.keys():
    if country_hash[key]['numberOfThings'] > max_things:
        max_things = country_hash[key]['numberOfThings']

for key in country_hash.keys():
    scale = country_hash[key]['numberOfThings']/max_things
    if(scale > 0.75):
        country_hash[key]['fillKey'] = 'HIGH'
    elif(scale <= 0.75 and scale > 0.50):
        country_hash[key]['fillKey'] = 'MEDIUM'
    elif(scale <= 0.50 and scale > 0.25):
        country_hash[key]['fillKey'] = 'LOW'
    else:
        country_hash[key]['fillKey'] = 'VERY_LOW'


print('There are %d unique time zones' %len(cnt))
print('Saving data')
with open('followerlocations.json', 'w') as outfile:
    json.dump(country_hash, outfile)

elapsed_time = time.time() - start_time
print ('Time elapsed: %d seconds' %elapsed_time)
