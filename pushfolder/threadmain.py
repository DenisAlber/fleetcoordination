#from long_polling import WaitThread
import requests
import json
import threading
import time
import websocket # In Zumi-Console: sudo pip install websocket-client
import Graph_Library as gr
import personalmap as pm
# import turning_functions as tf
import turning_class  as tf

from zumi.zumi import Zumi
from zumi.util.screen import Screen
from zumi.util.camera import Camera
from zumi.util.vision import Vision

zumi = Zumi()

vision = Vision()
screen=Screen()

IRB = 120
speed = 20
zumiID = "2" # Tims Zumi -> ID "1", Denis Zumi -> ID "2"
zumiMap = None
calculatedPath = []
inCrossing = False
scanRoute = False
qrmessage = ""
currentheading = ''
lastCrossing = ''
nextCrossing = ''
messagelist = list()
lock = threading.Lock()

# init
# startDirection = ''
# startCrossing = ''
endCrossing = ''
backedUpEndCrossing =''


def QRCapture():
    camera = Camera()
    #camera.start_camera()

    global scanRoute
    while True: 

        print("Kamera ist an!")
        while scanRoute:
            pass
            #frame = camera.capture()
            #qr_code = vision.find_QR_code(frame)
            #message = vision.get_QR_message(qr_code)

            # if(message != None):
            #     global qrmessage
            #     print(str(message))
            #     zumi.stop()
            #     qrmessage = message
                
        # camera.close()
        print("Kamera ist aus")
        while scanRoute == False:
            pass
        #camera.start_camera()

def DriveManager():
    
    global inCrossing
    global currentheading
    global calculatedPath
    global lastCrossing
    global nextCrossing
    global qrmessage
    global scanRoute
    global endCrossing
    
    while True:
        if qrmessage != "":
            break
        if len(calculatedPath) > 0 and inCrossing == False:
            
            print(inCrossing)
            GoStraight()
            inCrossing = True
            scanRoute = True
            #checkIfAbb
        if len(calculatedPath) > 0 and inCrossing == True:

            dirnumber = getCrossingDirection()
            #abgleich mit anderem auto
            print("dirnumber:" + str(dirnumber))
            #lock ?

            if dirnumber == 0:
                turningFunctions.turnLeft()
            elif dirnumber == 1:
                turningFunctions.turnStraight()
            elif dirnumber == 2:
                turningFunctions.turnRight()
            elif dirnumber == 3:
                turningFunctions.turnAround()
            currentheading = calculatedPath[0]['direction']
            lastCrossing = calculatedPath[0]['currentCrossing']
            nextCrossing = calculatedPath[0]['nextCrossing']
            
            msgPos = json.dumps({"zumiId" : zumiID, "currentCrossing" : lastCrossing, "nextCrossing" : nextCrossing, "direction" : currentheading})
            print("Send Zumi Position " + msgPos)
            ws.send(msgPos)

            calculatedPath.pop(0)

            if len(calculatedPath) == 0:
                msgRe = json.dumps({"release" : nextCrossing})
                # msg = '{release : ' + nextCrossing + '}'
                print("Release Zumi Target " + msgRe)
                ws.send(msgRe)


            inCrossing = False
            scanRoute = True
            #lock aufheben
    print("while over")
            
def ServerThread():
    global zumiMap
    zumiMap = gr.Graph()
    zumiMap = pm.initPersonalMap(zumiMap)
    """
    global startDirection
    global startCrossing
    global endCrossing
    """
    global currentheading
    global calculatedPath
    # global startDirection
    global nextCrossing
    global endCrossing
    global backedUpEndCrossing

    while True:
        print("Warte auf Instruktionen...")
        while currentheading == '' or nextCrossing == '' or endCrossing == '':
            ws.send(" ")
            time.sleep(2)
        print("Instruktion eingegangen!")
        
        # startDirection = 'East'
        # startCrossing = 'A'
        # endCrossing = 'C'
        # currentheading = startDirection
        calculatedPath = zumiMap.CalculatePath(currentheading,nextCrossing,endCrossing)
        backedUpEndCrossing = endCrossing
        endCrossing = ''
    


def getCrossingDirection():
    global currentheading
    global calculatedPath
    print(calculatedPath)
    if currentheading == 'North' and calculatedPath[0]['direction'] == 'West' or currentheading == 'East' and calculatedPath[0]['direction'] == 'North' or currentheading == 'South' and calculatedPath[0]['direction'] == 'East'or currentheading == 'West' and calculatedPath[0]['direction'] == 'South':
        return 0 #left
    elif currentheading == calculatedPath[0]['direction']:
        return 1 #straight
    elif currentheading == 'North' and calculatedPath[0]['direction'] == 'East' or currentheading == 'East' and calculatedPath[0]['direction'] == 'South' or currentheading == 'South' and calculatedPath[0]['direction'] == 'West' or currentheading == 'West' and calculatedPath[0]['direction'] == 'North':
        return 2 #right
    elif currentheading == 'North' and calculatedPath[0]['direction'] == 'South' or currentheading == 'East' and calculatedPath[0]['direction'] == 'West' or currentheading == 'South' and calculatedPath[0]['direction'] == 'North' or currentheading == 'West' and calculatedPath[0]['direction'] == 'East':
        return 3 #turnaround

def GoStraight():
    zumi.reset_gyro()
    heading = 0
    for x in range(2000): # Take steps
        
    
        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]

        if bottom_right_ir > IRB and bottom_left_ir > IRB:
            heading = heading           # do nothing
            
        elif bottom_left_ir < IRB and bottom_right_ir < IRB and x > 10:
            break
        elif bottom_left_ir < IRB and bottom_right_ir < IRB:
            zumi.stop()
            if turningFunctions.fixZumiPosition(lastCrossing,nextCrossing):
                screen.clear_display()
                screen.draw_text("Thank you")
                time.sleep(1.0)
                screen.clear_display()
                zumi.reset_gyro()
                heading = 0
                
            else:
                print("This Boy is gone")
                return False
            
        elif bottom_right_ir < IRB:
            heading += 0.5              # turn left
            
        elif bottom_left_ir < IRB:
            heading -= 0.5               # turn right
            
        if(qrmessage == ""):
            zumi.go_straight(speed, heading)
        else:
            break
    zumi.stop()
        
# print(data.get("id"))
def on_message(ws, message):
    # print(message)

    # prüfe ob Message ein JSON-String ist
    try:
        json.loads(message)
    except ValueError:
        print(message)
        return

    jsonMessage = json.loads(message)
    global endCrossing 
    global nextCrossing
    global currentheading
    global backedUpEndCrossing

    if("id" in jsonMessage and "isTarget" in jsonMessage):
        print(jsonMessage["id"])
        
        if(jsonMessage["isTarget"] == True):
            print("Ziel ist auf " + jsonMessage["id"] + " gesetzt!")
            
            endCrossing = jsonMessage["id"]

    if("id" in jsonMessage and "isBlocked" in jsonMessage):
        global zumiMap
        global calculatedPath
        if jsonMessage["isBlocked"] == True:    
            crossing = jsonMessage["id"]
            crossing = list(crossing)
            if(len(crossing) < 2):
                return
            print("Setzte Sperre für Strecke: " + jsonMessage["id"])
            zumiMap.SetLockForStreet(crossing[0], crossing[1])
            with lock:
                if(len(calculatedPath) > 0):
                    isMemberOfCalculatedPath = False
                    for path in calculatedPath:
                        if(path["currentCrossing"] == crossing[0] and path["nextCrossing"] == crossing[1]):
                            isMemberOfCalculatedPath = True
                    if isMemberOfCalculatedPath:
                        calculatedPath = zumiMap.CalculatePath(currentheading, nextCrossing, backedUpEndCrossing) # endcrossing neu bestimmen
                        print("Neuer Pfad: ")
                        print(calculatedPath)

        else:
            crossing = jsonMessage["id"]
            crossing = list(crossing)
            if(len(crossing) < 2):
                return
            zumiMap.ReleaseLockForStreet(crossing[0], crossing[1])
        

    if("zumiId" in jsonMessage and "id" in jsonMessage and "direction" in jsonMessage):
        if(jsonMessage["zumiId"] == zumiID):
            print("Setze Zumi Position..")
            crossing = jsonMessage["id"]
            crossing = list(crossing)
            if(len(crossing) < 2):
                return
            crossing.reverse()
            nextCrossing = crossing[0]
            currentheading = jsonMessage["direction"]
            print("Die nächste Kreuzung des Zumis ist: " + nextCrossing + ", " + currentheading)

    




def on_close(ws):
    print("### closed ###")


websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://fleetcoordination-zumi-cars.herokuapp.com/", on_message = on_message, on_close = on_close)
# ws = websocket.WebSocketApp("ws://localhost:3000", on_message = on_message, on_close = on_close)

# Start websocket client
wst = threading.Thread(target=ws.run_forever)
wst.daemon = True
wst.start()

# wait for connection
conn_timeout = 5
while not ws.sock.connected and conn_timeout:
    time.sleep(1)
    conn_timeout -= 1

print("Warte auf setzen der Position")
while nextCrossing == '' and currentheading == '':
    ws.send(json.dumps({"zumiId" : zumiID, "getOtherPosition" : "false"}))
    time.sleep(3)
    pass

turningFunctions = tf.turningFunctions(zumi, screen, time)
thread = threading.Thread(target = ServerThread)
thread2 = threading.Thread(target = DriveManager)
# thread3 = threading.Thread(target= QRCapture)
thread.start()
thread2.start()
# thread3.start()