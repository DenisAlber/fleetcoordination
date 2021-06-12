# from zumi.zumi import Zumi
# import time
# from zumi.util.screen import Screen

class turningFunctions:
    def __init__(self, zumi, screen, time):
        self.zumi = zumi
        self.screen = screen
        self.IRB = 120
        self.time = time
    # zumi = Zumi()
    # screen=Screen()
    # IRB = 120 #IR-Border, point where Black should begin

    def turnStraight(self):
        self.zumi.reset_gyro()
        heading = 0

        for x in range (40):

            ir_readings = self.zumi.get_all_IR_data()
            bottom_right_ir = ir_readings[1]
            bottom_left_ir = ir_readings[3]
            
            self.zumi.go_straight(20, heading)

            if bottom_left_ir > self.IRB or bottom_right_ir > self.IRB:
                break
            
        self.zumi.stop()

        for x in range(50):
            ir_readings = self.zumi.get_all_IR_data()
            bottom_right_ir = ir_readings[1]
            bottom_left_ir = ir_readings[3]

            if bottom_right_ir > self.IRB and bottom_left_ir > self.IRB:
                heading = heading           # do nothing
            elif bottom_left_ir < self.IRB and bottom_right_ir < self.IRB:
                break
            elif bottom_right_ir < self.IRB:
                heading += 1              # turn left
                
            elif bottom_left_ir < self.IRB:
                heading -= 1               # turn right
                
            
            self.zumi.go_straight(20, heading)
            
        self.zumi.stop()
        print("heading: " + str(heading))
        print("Gyro: " + str(self.zumi.read_z_angle()))
        return heading

    def fixZumiPosition(self, lastCrossing,nextCrossing):
        for x in range(5):
            self.zumi.play_note(30+x, note_duration=100)
            self.time.sleep(0.1)
        self.screen.clear_display()
        for x in range(15):

            if lastCrossing != None:
                self.screen.draw_text("Relocate between "+lastCrossing+ " and "+nextCrossing+" in " + str(15-x)+"s")
            elif lastCrossing == None:
                self.screen.draw_text("Place Zumi at    Start in "+ str(15-x) + "s")
            self.time.sleep(1.0)
            
        self.screen.clear_display()
        ir_readings = self.zumi.get_all_IR_data()
        bottom_right_ir = ir_readings[1]
        bottom_left_ir = ir_readings[3]

        if bottom_right_ir > self.IRB or bottom_left_ir > self.IRB:
            return True
        else:
            return False
                
    def turnAround(self):
        self.zumi.reset_gyro()
    
        self.zumi.left_u_turn(speed=20, step=6, delay=0.02)
        self.zumi.reset_gyro()
        heading = 0
        lf = False
        rf = False
        counter = 0
        for x in range (34):
            ir_readings = self.zumi.get_all_IR_data()
            bottom_right_ir = ir_readings[1]
            bottom_left_ir = ir_readings[3]
        
            if bottom_right_ir > self.IRB and bottom_left_ir > self.IRB:
                heading = heading           # do nothing
                lf = False
                rf = False
                
            
            elif bottom_right_ir < self.IRB and lf == False:
                heading += (3.5 - counter *0.1)              # turn left
                rf = True
                counter = counter +1
                
            elif bottom_left_ir < self.IRB and rf == False:
                heading -= (3.5 - counter * 0.1)               # turn right
                lf = True 
                counter = counter +1
        
            self.zumi.go_straight(10, heading)
                
        self.zumi.stop()
        return heading


    def turnRight(self):
        self.zumi.reset_gyro()
        heading = 0
        
        for x in range (1000):

            ir_readings = self.zumi.get_all_IR_data()
            bottom_right_ir = ir_readings[1]
            bottom_left_ir = ir_readings[3]
            
            self.zumi.go_straight(20, heading)
            
            if heading > -73:
                heading -= 4
            


            if heading < -75 and (bottom_left_ir > self.IRB or bottom_right_ir > self.IRB):
                self.zumi.stop()
                
                break
        
        counter = 0
        lf = False
        rf = False
        for x in range (34):  #bisheriges optimum 34 steps
            ir_readings = self.zumi.get_all_IR_data()
            bottom_right_ir = ir_readings[1]
            bottom_left_ir = ir_readings[3]
        
            if bottom_right_ir > self.IRB and bottom_left_ir > self.IRB:
                heading = heading           # do nothing
                lf = False
                rf = False
                
            
            elif bottom_right_ir < self.IRB and lf == False:
                heading += (3.5 - counter *0.1)              # turn left
                rf = True
                counter = counter +1
                
            elif bottom_left_ir < self.IRB and rf == False:
                heading -= (3.5 - counter * 0.1)               # turn right
                lf = True 
                counter = counter +1
        
            self.zumi.go_straight(10, heading)
                
        self.zumi.stop()
        print("heading: " + str(heading))
        print("Gyro: " + str(self.zumi.read_z_angle()))
        return heading



    def turnLeft(self):

        self.zumi.reset_gyro()
        heading = 0
        
        
        for x in range (40):

            ir_readings = self.zumi.get_all_IR_data()
            bottom_right_ir = ir_readings[1]
            bottom_left_ir = ir_readings[3]
            
            self.zumi.go_straight(20, heading)

            if bottom_left_ir > self.IRB or bottom_right_ir > self.IRB:
                self.zumi.stop()
                break
        
        for x in range(14):
            ir_readings = self.zumi.get_all_IR_data()
            bottom_right_ir = ir_readings[1]
            bottom_left_ir = ir_readings[3]

            if bottom_right_ir > self.IRB and bottom_left_ir > self.IRB:
                heading = heading           # do nothing
            elif bottom_left_ir < self.IRB and bottom_right_ir < self.IRB:
                break
            elif bottom_right_ir < self.IRB:
                heading += 1              # turn left
                
            elif bottom_left_ir < self.IRB:
                heading -= 1               # turn right
                
            
            self.zumi.go_straight(20, heading)
        self.zumi.stop()
        for x in range (100):

            ir_readings = self.zumi.get_all_IR_data()
            bottom_right_ir = ir_readings[1]
            bottom_left_ir = ir_readings[3]
            
            self.zumi.go_straight(20, heading)
            
            if heading < 73:
                heading += 4
                


            if heading > 73 and (bottom_left_ir > self.IRB or bottom_right_ir > self.IRB):
                self.zumi.stop()
            
                break
        counter = 0
        lf = False
        rf = False
        for x in range (34):
            ir_readings = self.zumi.get_all_IR_data()
            bottom_right_ir = ir_readings[1]
            bottom_left_ir = ir_readings[3]
            
            if bottom_right_ir > self.IRB and bottom_left_ir > self.IRB:
                heading = heading           # do nothing
                lf = False
                rf = False
                
            
            elif bottom_right_ir < self.IRB and lf == False:
                heading += (3.5 - counter *0.1)              # turn left
                rf = True
                counter = counter +1
                
            elif bottom_left_ir < self.IRB and rf == False:
                heading -= (3.5 - counter * 0.1)               # turn right
                lf = True 
                counter = counter +1
            
            self.zumi.go_straight(10, heading)
        self.zumi.stop()
        print("heading: " + str(heading))
        print("Gyro: " + str(self.zumi.read_z_angle()))
        return heading
            
        









    