#!/usr/bin/env python3

from hamming_code import HammingCode
from stack_machine import StackMachine
from robot import *


def run():
    # the execution of all code shall be started from within this function
    #print("Hello World!")
    sm = StackMachine()
    hm = HammingCode()
    robot = Robot()
    ##########
    co = robot.scroll_step()
    c1 = 1
    bit = []
    if(co==1):
        uncorr = 0
        while(1):
            if c1==1:
                x = robot.sm.position
                print("\n")
                print("Reading Codeword......")  
                for j in range(11):
                    x = x + 57.1
                    robot.sensor_step(x)
                    bit.append(robot.read_value())
                #robot.ev3.screen.draw_text(40, 50, bit)
                print("Recieved Codeword", bit)
                out = hm.decode(bit)
                #print("Decoded Codeword", out[0])
                print("Decoded Codeword: ",out[0])
                print("Hamming Code status: ", out[1])
                bit = []
                robot.sensor_reset()
                if(str(out[0]) == "None" and uncorr <= 3):
                    print("Recieved Codeword incorrect: Re-Reading.....")
                    uncorr = uncorr+1
                    pass
                elif(uncorr == 4):
                    uncorr = 0
                    print("Cannot be corrected")
                    print("Skipping this codeword")
                    var = robot.scroll_step()
                else:
                    uncorr = 0
                    sm_state = sm.do(out[0])
                    print("Stack Machine status:", sm_state)
                    if (str(sm_state) == "SMState.ERROR"):
                        print("TOP ELEMENT =", sm.top())
                        sm.stack = []
                        temp = 0 
                        c1 = 0
                    elif(str(sm_state) == "SMState.STOPPED"):
                        print("TOP ELEMENT =", sm.top())
                        sm.stack = []
                        temp = 1
                        c1 = 0
                    else:
                        temp = 1
                        print("TOP ELEMENT =", sm.top())
                        print("Current Elements in Stack", sm.stack)
                        c1 = robot.scroll_step()
                            
                                    
            else:
                if temp == 1:
                    print("Card Completed.")
                    print("If you want to add next card: Put it and Press 1 else To stop Press 0")
                    card = input()
                    if (str(card)=="1"):
                        c1 = 1
                        co = robot.scroll_step()
                        bit = []
                    else:
                        break
                else:
                    print("ERROR OCCURED")
                    break
                    
    else:
        print("No Code-words detected")
        #########
        #hamming code
        
        
            


if __name__ == '__main__':
    run()
