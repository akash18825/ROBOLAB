#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import time


class Robot:
    """
    -- TEMPLATE --
    This class provides logic for moving the sensor and scrolling the bar code card
    """
    def __init__(self) -> None:
        self.cs = ev3.ColorSensor("in1")
        self.sm= ev3.LargeMotor("outA")
        self.fm= ev3.LargeMotor("outB")
        self.cs.mode = 'RGB-RAW'
        
    def CS_threshold(self, rgb):
        res=""
        if(rgb[0]>rgb[1] and rgb[0]>rgb[2]):
            res="red"
        else:
            if(rgb[1]>230):
                res="white"
            else:
                res="black"
        return res

    def sensor_step(self, x):
        """
        Moves the sensor one step to read the next bar code value
        """
        
        # implementation
        #self.sm.position = self.sm.position+55
        self.sm.run_to_abs_pos(position_sp = x, speed_sp=100)
        self.sm.wait_while('running')
        time.sleep(0.1) # original value 0.1

    def sensor_reset(self):
        """
        Resets the sensor position
        """
        # implementation
        while(1):
            self.sm.run_timed(time_sp=3000,speed_sp=-250,stop_action="brake")
            values=self.cs.bin_data("hhh")
            if(self.CS_threshold(values)=="red"):
                self.sm.stop()
                pos = self.sm.position
                break

    def scroll_step(self):
        """
        Moves the bar code card to the next line.
        """
        # implementation
        flag=1
        while(1):
            iv = self.fm.position
            self.fm.run_timed(time_sp=3000,speed_sp=150)
            values=self.cs.bin_data("hhh")
            if(self.CS_threshold(values)=="white"):
                #self.fm.stop()
                break
        while(1):
            self.fm.run_timed(time_sp=3000,speed_sp=150)
            values=self.cs.bin_data("hhh")
            if(self.CS_threshold(values)=="red" and self.fm.position<iv+300):
                #x1=self.fm.position
                #self.fm.run_to_abs_pos(position_sp = x1, speed_sp=150)
                self.fm.stop()
                self.fm.run_timed(time_sp=150,speed_sp=150)
                pos=self.fm.position
                break
            elif(self.fm.position>iv+100): # original value= 150
                self.fm.stop()
                pos=self.fm.position
                print("Code ended")
                flag=0
                break
        return flag

    def read_value(self) -> int:
        """
        Reads a single value, converts it and returns the binary expression
        :return: int
        """
        # implementation
        values=self.cs.bin_data("hhh")
        res = 0
        if (self.CS_threshold(values)=="black"):
            res = 1
        elif(self.CS_threshold(values)=="white"):
            res = 0
        return res
