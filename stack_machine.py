#!/usr/bin/env python3

from enum import IntEnum
from typing import List, Tuple, Union
from ctypes import c_ubyte
import ev3dev.ev3 as ev3
import time


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class SMState(IntEnum):
    """
    Return codes for the stack machine
    """
    RUNNING = 1
    STOPPED = 0
    ERROR = -1


class StackMachine:
    """
    Implements the 8-bit stack machine according to the specification
    """

    def __init__(self) -> None:
        """
        Initializes the class StackMachine with all values necessary.
        """
        self.overflow = False
        self.stack = []

    def pop(self):
        if len(self.stack) != 0:
            element = self.stack[len(self.stack)-1]
            del self.stack[-1]
            return element
        else:
            pass
            #empty stack
    def push(self, element):
        self.stack.append(element)
    def instruction(self, data):
        stack_element = len(self.stack)-1
        if data == [0, 0, 0, 0]:
            print("Instruction executed: STOP")
            return SMState.STOPPED
        elif data == [0, 0, 0, 1]:
            #DUP
            print("Instruction executed: DUP")
            if (len(self.stack)!=0):
                x1 = self.pop()
                #self.list_to_decimal
                self.push(x1)
                self.push(x1)
                return SMState.RUNNING
            else:
                print("ERROR MESSAGE: not enough items")
                return SMState.ERROR
        elif data == [0, 0, 1, 0]:
            #DEL
            print("Instruction executed: DEL")
            if (len(self.stack)!=0):
                x1 = self.pop()
                return SMState.RUNNING
            else:
                print("ERROR MESSAGE: not enough items")
                return SMState.ERROR
        elif data == [0, 0, 1, 1]:
                #SWP
            print("Instruction executed: SWP")
            if (len(self.stack)>=2):
                x1 = self.pop()
                x2 = self.pop()
                self.push(x1)
                self.push(x2)
                return SMState.RUNNING
            else:
                print("ERROR MESSAGE: not enough items")
                return SMState.ERROR
        elif data ==[0, 1, 0, 0]:
            #ADD
            print("Instruction executed: ADD")
            if (len(self.stack)>=2):
                x1 = self.pop()
                x2 = self.pop()
                if (isinstance(x1, int) and isinstance(x2, int) and x1+x2<256):
                    self.push(x1+x2)
                    return SMState.RUNNING
                elif (isinstance(x1, int) and isinstance(x2, int) and x1+x2>255):
                    self.overflow = True
                    self.push((x1+x2)-256)
                    return SMState.RUNNING
                else:
                    print("ERROR MESSAGE: char can't be added")
                    return SMState.ERROR
            else:
                print("ERROR MESSAGE: not enough items")
                return SMState.ERROR 

        elif data == [0, 1, 0, 1]:
            #SUB
            print("Instruction executed: SUB")
            if (len(self.stack)>=2):
                x2 = self.pop()
                x1 = self.pop()
                if (isinstance(x1, int) and isinstance(x2, int) and x1-x2>=0):
                    self.push(x1-x2)
                    return SMState.RUNNING
                elif (isinstance(x1, int) and isinstance(x2, int) and x1-x2 < 0):
                    self.overflow = True
                    self.push(x2-x1)
                    return SMState.RUNNING
                else:
                    print("ERROR MESSAGE: char can't be Subtracted")
                    return SMState.ERROR
            else:
                print("ERROR MESSAGE: not enough items")
                return SMState.ERROR
        elif data == [0, 1, 1, 0]:
                #MUL
            print("Instruction executed: MUL")
            if (len(self.stack)>=2):
                x1 = self.pop()
                x2 = self.pop()
                if (isinstance(x1, int) and isinstance(x2, int) and x2*x1<256):
                    self.push(x2*x1)
                    return SMState.RUNNING
                elif (isinstance(x1, int) and isinstance(x2, int) and x1*x2>255):
                    self.overflow = True
                    tmp = (x2*x1)%256
                    self.push(tmp)
                    return SMState.RUNNING
                else:
                    print("ERROR MESSAGE: char can't be multiplied")
                    return SMState.ERROR
            else:
                print("ERROR MESSAGE: not enough items")
                return SMState.ERROR
        elif data ==[0, 1, 1, 1]:
                #DIV
            print("Instruction executed: DIV")
            if (len(self.stack)>=2):
                x1 = self.pop()
                x2 = self.pop()
                if (isinstance(x1, int) and isinstance(x2, int) and x1!=0):
                    self.push(x2//x1)
                    return SMState.RUNNING
                else:
                    print("ERROR MESSAGE: invalid range")
                    return SMState.ERROR
            else:
                print("ERROR MESSAGE: not enough items")
                return SMState.ERROR
        elif data == [1, 0, 0, 0]:
                #EXP
            print("Instruction executed: EXP")
            if (len(self.stack)>=2):
                x1 = self.pop()
                x2 = self.pop()
                if (isinstance(x1, int) and isinstance(x2, int) and x2**x1<256):
                    self.push(x2**x1)
                    return SMState.RUNNING
                elif (isinstance(x1, int) and isinstance(x2, int) and x2**x1>255):
                    self.overflow = True
                    tmp = (x2*x1)%256
                    self.push(tmp)
                    return SMState.RUNNING
                else:
                    print("ERROR MESSAGE: char can't be exponented")
                    return SMState.ERROR
            else:
                print("ERROR MESSAGE: not enough items")
                return SMState.ERROR
        elif data ==[1, 0, 0, 1]:
                #MOD
            print("Instruction executed: MOD")
            if (len(self.stack)>=2):
                x1 = self.pop()
                x2 = self.pop()
                if (isinstance(x1, int) and isinstance(x2, int)):
                    self.push(x2%x1)
                    return SMState.RUNNING
                else:
                    print("ERROR MESSAGE: char don't has mod")
                    return SMState.ERROR
            else:
                print("ERROR MESSAGE: not enough items")
                return SMState.ERROR 
        elif data == [1, 0, 1, 0]:
                #SHL
            print("Instruction executed: SHL")
            if (len(self.stack)>=2):
                x1 = self.pop()
                x2 = self.pop()
                if (isinstance(x1, int) and isinstance(x2, int) and (x2<<x1)<256):
                    self.push(x2<<x1)
                    return SMState.RUNNING
                elif (isinstance(x1, int) and isinstance(x2, int) and x2<<x1>255):
                    self.overflow = True
                    tmp = (x2*x1)%256
                    self.push(tmp)
                    return SMState.RUNNING
                else:
                    print("ERROR MESSAGE: char can't be shifted")
                    return SMState.ERROR
            else:
                print("ERROR MESSAGE: not enough items")
                return SMState.ERROR   
        elif data ==[1, 0, 1, 1]:
                #shr
            print("Instruction executed: SHR")
            if (len(self.stack)>=2):
                x1 = self.pop()
                x2 = self.pop()
                if (isinstance(x1, int) and isinstance(x2, int)):
                    self.push(x2>>x1)
                    return SMState.RUNNING
                else:
                    print("ERROR MESSAGE: char can't be shifted")
                    return SMState.ERROR
            else:
                print("ERROR MESSAGE: not enough items")
                return SMState.ERROR
        elif data == [1, 1, 0, 0]:
            #HEX
            print("Instruction executed: HEX")
            if (len(self.stack)>=2):
                x1 = str(self.pop())
                x2 = str(self.pop())
                valid = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F")
                if x1 in valid and x2 in valid:
                    merge = "0x" + x1+x2
                    self.push(int(merge, 16))
                    return SMState.RUNNING
                else:
                    print("ERROR MESSAGE: invalid range")
                    return SMState.ERROR
            else:
                print("ERROR MESSAGE: not enough items")
                return SMState.ERROR
        elif data == [1, 1, 0, 1]:
            #fac
            print("Instruction executed: FAC")
            if (len(self.stack)>=1):
                x1 = self.pop()
                if (isinstance(x1, int)):
                    fact = 1
                    for s in range(x1):
                        fact = fact*(s+1)
                    if (fact < 256):
                        self.push(fact)
                        self.overflow = False
                        return SMState.RUNNING
                    else:
                        self.overflow = True
                        tmp = fact%256
                        self.push(tmp)
                        return SMState.RUNNING
                else:
                    print("ERROR MESSAGE: char don't have factorial")
                    return SMState.ERROR
            else:
                print("ERROR MESSAGE: not enough items")
                return SMState.ERROR
        elif data == [1, 1, 1, 0]:
            #1s comp
            print("Instruction executed: COMP")
            if (len(self.stack)>=1):
                x1 = self.pop()
                if (isinstance(x1, int)):
                    self.push(255-x1)
                    return SMState.RUNNING
                else:
                    print("ERROR MESSAGE: char can't be complemented")
                    return SMState.ERROR
            else:
                print("ERROR MESSAGE: not enough items")
                return SMState.ERROR   
        elif data ==[1, 1, 1, 1]:
            print("Instruction executed: XOR")
            if (len(self.stack)>=2):
                x1 = self.pop()
                x2 = self.pop()
                if (isinstance(x1, int)) and (isinstance(x2, int)):
                    self.push(x2^x1)
                    return SMState.RUNNING
                else:
                    print("ERROR MESSAGE: char can't be XOR'd")
                    return SMState.ERROR
            else:
                print("ERROR MESSAGE: not enough items")
                return SMState.ERROR
        else:
            pass
            #default

    def characters(self, word):
        self.flag = 0
        if (word == [0, 0, 0, 0, 1]): #SPEAK
            print("Executing speak")
            if (len(self.stack)>=2):
                x1 = self.pop()
                speak=[]
                if (isinstance(x1, int) and len(self.stack) >= x1):
                    for i in range(x1):
                        #ch = self.pop()
                        #ev3.Sound.speak(ch)
                        speak.append(self.pop())
                    speak_str=''.join([str(i) for i in speak])
                    print(speak_str)
                    print("\n")
                    print("SPEAKING....")
                    for i in range(len(speak)):
                        time.sleep(1)
                        ev3.Sound.speak(speak[i])
                        print(speak[i])
                        time.sleep(1.5) #original= 2
                    
                    return SMState.RUNNING
                else:
                    if (isinstance(x1, str)):
                        print("ERROR MESSAGE: Top element is not integer")
                    else:
                        print("ERROR MESSAGE: not enough items")
                    self.flag = 1
                    #return SMState.ERROR
            else:
                print("ERROR MESSAGE: not enough items")
                self.flag = 1
                #return SMState.ERROR

        elif (word == [0, 0, 0, 1, 0]):
            self.push(" ")
        elif (word == [0, 0, 1, 0, 0]):
            self.push("A")
        elif (word == [0, 0, 1, 0, 1]):
            self.push("B")
        elif (word == [0, 0, 1, 1, 0]):
            self.push("C")
        elif (word == [0, 0, 1, 1, 1]):
            self.push("D")
        elif (word == [0, 1, 0, 0, 0]):
            self.push("E")
        elif (word == [0, 1, 0, 0, 1]):
            self.push("F")
        elif (word == [0, 1, 0, 1, 0]):
            self.push("G")
        elif (word == [0, 1, 0, 1, 1]):
            self.push("H")
        elif (word == [0, 1, 1, 0, 0]):
            self.push("I")
        elif (word == [0, 1, 1, 0, 1]):
            self.push("J")
        elif (word == [0, 1, 1, 1, 0]):
            self.push("K")
        elif (word == [0, 1, 1, 1, 1]):
            self.push("L")
        elif (word == [1, 0, 0, 0, 0]):
            self.push("M")
        elif (word == [1, 0, 0, 0, 1]):
            self.push("N")
        elif (word == [1, 0, 0, 1, 0]):
            self.push("O")
        elif (word == [1, 0, 0, 1, 1]):
            self.push("P")
        elif (word == [1, 0, 1, 0, 0]):
            self.push("Q")
        elif (word == [1, 0, 1, 0, 1]):
            self.push("R")
        elif (word == [1, 0, 1, 1, 0]):
            self.push("S")
        elif (word == [1, 0, 1, 1, 1]):
            self.push("T")
        elif (word == [1, 1, 0, 0, 0]):
            self.push("U")
        elif (word == [1, 1, 0, 0, 1]):
            self.push("V")
        elif (word == [1, 1, 0, 1, 0]):
            self.push("W")
        elif (word == [1, 1, 0, 1, 1]):
            self.push("X")
        elif (word == [1, 1, 1, 0, 0]):
            self.push("Y")
        elif (word == [1, 1, 1, 0, 1]):
            self.push("Z")
        else:
            #NOP
            print("Instruction executed: NO Operation")
            

    def do(self, code_word: Tuple[int, ...]) -> SMState:
        """
        Processes the entered code word by either executing the instruction or pushing the operand on the stack.

        Args:
            code_word (tuple): Command for the stack machine to execute
        Returns:
            SMState: Current state of the stack machine
        """
        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        decoded_word = 0
        code_word = list(code_word)
        self.overflow = False
        if (code_word[0] == 0):
            if(code_word[1] == 0):
                decoded_word = code_word[2:6]
                dec = 0
                for i in decoded_word:
                    dec = (dec << 1) | i
                print("Operand Read: ", dec)
                self.push(dec)
                return SMState.RUNNING
            elif (code_word[1] == 1):
                state = self.instruction(code_word[2:6])
                return  state
        elif(code_word[0]):
            self.characters(code_word[1:6])
            if (self.flag == 1):
                return SMState.ERROR
            else:
                return SMState.RUNNING

    def top(self) -> Union[None, str, Tuple[int, int, int, int, int, int, int, int]]:
        """
        Returns the top element of the stack.

        Returns:
            union: Can be tuple, str or None
        """


        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        if (len(self.stack) != 0):
            if (type(self.stack[-1])) == int:
                binary = (format(self.stack[-1], '08b'))
                bit8_int = [eval(i) for i in list(binary)]
                bin_tuple = tuple(bit8_int)
                return bin_tuple
            elif ((type(self.stack[-1])) == str):
                return (self.stack[-1])
        else:
            return None

#h = StackMachine()
#x = h.do((0, 0, 1, 1, 1, 1))
#x = h.do((0, 0, 0, 0, 1, 1))
#y = h.do((0, 1, 1, 0, 0, 0))
#y = h.do((0, 0, 1, 1, 1, 1))
#y = h.do((0, 1, 0, 1, 1, 0))
#t = h.top()
#print(t)
#y = h.do((0, 0, 0, 0, 0, 1))
#d = h.do((0, 1, 0, 1, 0, 1))
#print(c)
#print(h.top())
#print(h.overflow)
#d = h.do((0, 0, 1, 1, 1, 1))
#d = h.do((0, 1, 0, 1, 0, 0))
#d = h.do((0, 0, 1, 1, 1, 1))
#d = h.do((0, 1, 0, 1, 0, 0))
#print(h.stack)
#d = h.do((0, 0, 0, 0, 0, 1))
#d = h.do((0, 1, 0, 1, 0, 0))
#print(h.stack)
#print(h.top())
#d = h.do((1, 0, 1, 0, 0, 1))
#d = h.do((0, 1, 0, 1, 1, 0))
#d = h.do((0, 0, 1, 1, 1, 1))
#d = h.do((0, 0, 0, 1, 1, 0))
#d = h.do((1, 0, 0, 0, 0, 1))
#d = h.do((0, 1, 0, 1, 0, 0))

#d = h.do((0, 1, 1, 1, 0, 0))
#d = h.do((0, 0, 0, 0, 0, 1))
#d = h.do((0, 1, 0, 1, 1, 1))
#print(d)
#print(h.stack)
#y = h.do((0, 0, 0, 0, 1, 0))
#d = x.do((1, 0, 0, 0, 0, 1))

