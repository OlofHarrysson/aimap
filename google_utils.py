from pathlib import Path
import requests


def read_api_key():
  api_path = Path("keys.txt")
  assert api_path.exists(), f"API-key file doesn't exist at {api_path}"
  with open(api_path) as f:
    key = f.read()
  return key


def get_location(company_name):
  api_key = read_api_key()
  url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
  response = requests.get(url + 'query=' + company_name + '&key=' + api_key)
  response = response.json()

  if len(response['results']) != 0:
    results = response['results'][0]
    return results['geometry']['location']
