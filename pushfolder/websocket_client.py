import requests
import json
import threading
import time
import websocket

# url = 'http://192.168.10.80:3000/Zumi'
# x = requests.get(url)
# data = json.loads(x.text)


# print(data.get("id"))
def on_message(ws, message):
    print(message)

def on_close(ws):
    print("### closed ###")

# def LongPolling():
#     # url = 'http://192.168.10.80:3000/Zumi'
#     url = 'http://192.168.178.108:3000/Zumi'
 
#     x = requests.get(url)
#     data = json.loads(x.text)
#     print(data.get("id") + " " + str(data.get("isBlocked")))
#     LongPolling()


def SendMessageThread():
    for x in range(100, 150):
        # print(x)
        ws.send('{"node1":"A", "node2":"B"}')
        time.sleep(1)


websocket.enableTrace(True)
# ws = websocket.WebSocketApp("wss://fleetcoordination-zumi-cars.herokuapp.com/", on_message = on_message, on_close = on_close)

ws = websocket.WebSocketApp("ws://localhost:3000", on_message = on_message, on_close = on_close)
wst = threading.Thread(target=ws.run_forever)
wst.daemon = True
wst.start()

# wait for connection
conn_timeout = 5
while not ws.sock.connected and conn_timeout:
    time.sleep(1)
    conn_timeout -= 1

# thread = threading.Thread(target = LongPolling)
thread2 = threading.Thread(target = WaitThread)
# thread.start()
thread2.start()
print("wait...")