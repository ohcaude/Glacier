import json
import requests 

url = 'https://api.planet.com/v0/orders/'
usr = '69c1c54d10324eb58c5677cc8737fc0c'
pss = 'ocbiYWN5S6D2'
r = requests.get(url, auth=(usr,pss))

print(r.headers)
#print(r.text) # or r.json()

data = json.loads(r.text)


for order in data:
    print((order['name'],order['download_url']))

