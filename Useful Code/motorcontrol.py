from zumi.zumi import Zumi
import time

zumi = Zumi()

zumi.calibrate_gyro()
zumi.control_motors(2,2)
brir = False
blir = False
counter = 0
for x in range (40):
    if counter == 2:
        break

    ir_readings = zumi.get_all_IR_data()
    bottom_right_ir = ir_readings[1]
    bottom_left_ir = ir_readings[3]
    
    
    print("step")

    if bottom_left_ir > 130:
        blir = True
        print("left")
    if bottom_right_ir > 130:
        brir = True
        print("right")

    if brir and blir:
        counter = counter +1
        
    

zumi.stop()



ir_readings = zumi.get_all_IR_data()
bottom_right_ir = ir_readings[1]
bottom_left_ir = ir_readings[3]

print(bottom_right_ir)
print(bottom_left_ir)
if bottom_right_ir < 130:
    zumi.control_motors(-2,0)
    while(bottom_right_ir):
        ir_readings = zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
print(bottom_right_ir)
print(bottom_left_ir)
zumi.stop()

ir_readings = zumi.get_all_IR_data()
bottom_right_ir = ir_readings[1]
bottom_left_ir = ir_readings[3]

if bottom_left_ir < 130:
    zumi.control_motors(0,-2)
    while(bottom_left_ir):
        ir_readings = zumi.get_all_IR_data()
        bottom_left_ir = ir_readings[3]

ir_readings = zumi.get_all_IR_data()
bottom_right_ir = ir_readings[1]
bottom_left_ir = ir_readings[3]


print(bottom_right_ir)
print(bottom_left_ir)
zumi.stop()

   



"""
zumi.control_motors(0,2)

time.sleep(10)
zumi.stop()
"""