from zumi.zumi import Zumi
import time

zumi = Zumi()

zumi.calibrate_gyro()
#zumi.control_motors(2,2)
brir = False
blir = False
counter = 0


for x in range (40):
    
    ir_readings = zumi.get_all_IR_data()        #ir daten holen
    bottom_right_ir = ir_readings[1]
    bottom_left_ir = ir_readings[3]
    
    
    if bottom_left_ir > 130:            #checken ob linker sensor auf schwarz
        blir = True
        
    if bottom_right_ir > 130:           #gleiches für rechts
        brir = True
        

    if brir and blir and bottom_right_ir < 110 and bottom_left_ir < 110 :   #wenn beide senoren auf scharz waren und wieder runter sind
        break
    zumi.go_straight(5,0)   #langsames fahren
        
    

zumi.stop()



ir_readings = zumi.get_all_IR_data()        #ausgabe werte nach schleife, für debugging
bottom_right_ir = ir_readings[1]
bottom_left_ir = ir_readings[3]

print(bottom_right_ir)
print(bottom_left_ir)



zumi.control_motors(-2,0)                   #rechtes rad rückwärts
while(bottom_right_ir < 130):               #so lange motor drehen bis rechter sensor auf schwarz
    ir_readings = zumi.get_all_IR_data()
    bottom_right_ir = ir_readings[1]

zumi.stop()

print("after right")        #debug
print(bottom_right_ir)
print(bottom_left_ir)


ir_readings = zumi.get_all_IR_data() # refresh values
bottom_right_ir = ir_readings[1]
bottom_left_ir = ir_readings[3]

zumi.control_motors(0,-2)               #gleiches ding für links
while(bottom_left_ir < 130):
    print(bottom_left_ir)
    ir_readings = zumi.get_all_IR_data()
    bottom_left_ir = ir_readings[3]
zumi.stop()

ir_readings = zumi.get_all_IR_data()
bottom_right_ir = ir_readings[1]
bottom_left_ir = ir_readings[3]


print(bottom_right_ir)
print(bottom_left_ir)


   



"""
zumi.control_motors(0,2)

time.sleep(10)
zumi.stop()
"""