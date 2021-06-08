import requests
import json
import threading
import time

# url = 'http://192.168.10.80:3000/Zumi'
# x = requests.get(url)
# data = json.loads(x.text)


# print(data.get("id"))

def LongPolling():
    # url = 'http://192.168.10.80:3000/Zumi'
    url = 'http://192.168.178.108:3000/Zumi'
 
    x = requests.get(url)
    data = json.loads(x.text)
    print(data.get("id") + " " + str(data.get("isBlocked")))
    LongPolling()

def WaitThread():
    for x in range(100, 150):
        print(x)
        time.sleep(0.1)

thread = threading.Thread(target = LongPolling)
thread2 = threading.Thread(target = WaitThread)
thread.start()
thread2.start()
print("wait...")