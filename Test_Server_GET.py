import requests
import json

# url = 'http://localhost:3000/Zumi'
url = 'http://192.168.10.80:3000/Zumi' # Am besten nochmal über die Konsole die IP des Rechners ausgeben lassen und ggf. korrigieren

x = requests.get(url)
data = json.loads(x.text)

print(data.get("name"))