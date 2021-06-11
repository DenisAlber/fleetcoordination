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

def SendMessageThread():
    while True:
        # print(x)
        # ws.send('{"node1":"A", "node2":"B"}')
        
        ws.send('{"zumiId":"2"}')
        time.sleep(2)

def SendMessageThreadTwo():
    while True:
        # print(x)
        ws.send('{"node1":"B", "node2":"C"}')
        time.sleep(1)


websocket.enableTrace(True)
# ws = websocket.WebSocketApp("wss://fleetcoordination-zumi-cars.herokuapp.com/", on_message = on_message, on_close = on_close)
ws = websocket.WebSocketApp("ws://localhost:3000", on_message = on_message, on_close = on_close)

# Start websocket client
wst = threading.Thread(target=ws.run_forever)
wst.daemon = True
wst.start()

# wait for connection
conn_timeout = 5
while not ws.sock.connected and conn_timeout:
    time.sleep(1)
    conn_timeout -= 1

thread = threading.Thread(target = SendMessageThread)
# thread2 = threading.Thread(target = SendMessageThreadTwo)
thread.start()
# thread2.start()
print("wait...")