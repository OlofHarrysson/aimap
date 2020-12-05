from googlemaps import Client as Googlemaps
from google_utils import read_api_key
# gmaps = Googlemaps(api_key)
# address = 'Räntmästaregatan 28B 416 58 Göteborg Sweden'
# lat, lng = gmaps.address_to_latlng(address)
# print(lat, lng)
# print('#########################')

import requests, json 
  
# enter your api key here 
api_key = read_api_key()

# url variable store url 
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
  
# The text string on which to search 
##query = input('Search query: ') 
query = 'Skyqraft'
  
# get method of requests module 
# return response object 
r = requests.get(url + 'query=' + query +
                        '&key=' + api_key) 
  
# json method of response object convert 
#  json format data into python format data 
x = r.json() 
  
# now x contains list of nested dictionaries 
# we know dictionary contain key value pair 
# store the value of result key in variable y 
y = x['results'] 
  
# keep looping upto length of y 
for i in range(len(y)): 
      
    # Print value corresponding to the 
    # 'name' key at the ith index of y 
    print(y[i]['name']) 
    print(y[i]['place_id'])