# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 22:07:54 2022

@author: akash
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from enum import Enum
from typing import List, Tuple, Union


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class HCResult(Enum):
    """
    Return codes for the Hamming Code interface
    """
    VALID = 'OK'
    CORRECTED = 'FIXED'
    UNCORRECTABLE = 'ERROR'


class HammingCode:
    """
    Provides decoding capabilities for the specified Hamming Code
    """

    def __init__(self):
        """
        Initializes the class HammingCode with all values necessary.
        """
        self.total_bits = 10  # n
        self.data_bits = 6  # k
        self.parity_bits = 4  # r

        # Predefined non-systematic generator matrix G'
        gns = [[1,1,1,0,0,0,0,1,0,0],
               [0,1,0,0,1,0,0,1,0,0],
               [1,0,0,1,0,1,0,0,0,0],
               [0,0,0,1,0,0,1,1,0,0],
               [1,1,0,1,0,0,0,1,1,0],
               [1,0,0,1,0,0,0,1,0,1]]

        # Convert non-systematic G' into systematic matrices G, H
        self.g = self.__convert_to_g(gns)
        self.h = self.__derive_h(self.g)


    def __convert_to_g(self, gns: List):
        """
        Converts a non-systematic generator matrix into a systematic

        Args:
            gns (List): Non-systematic generator matrix
        Returns:
            list: Converted systematic generator matrix
        """
        

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        generatorMatrix = gns
        def rr(r1,r2,matrix):
             upd = []
             for i in range(len(matrix[0])):
                 item = generatorMatrix[r1-1][i]-generatorMatrix[r2-1][i]
                 upd.append(abs(item))
             generatorMatrix[r1-1]=upd
              
        rr(3,1,generatorMatrix)  
        rr(5,1,generatorMatrix)
        rr(6,1,generatorMatrix)
        rr(1,2,generatorMatrix)
        rr(3,2,generatorMatrix)
        rr(6,2,generatorMatrix)
        rr(1,3,generatorMatrix)
        rr(5,3,generatorMatrix)
        rr(6,3,generatorMatrix)
        rr(1,4,generatorMatrix)
        rr(3,4,generatorMatrix)
        rr(2,5,generatorMatrix)
        rr(3,5,generatorMatrix)
        rr(1,6,generatorMatrix)
        rr(2,6,generatorMatrix)
        rr(5,6,generatorMatrix)
        
        return generatorMatrix

    def __derive_h(self, g: List):
        """
        This method executes all steps necessary to derive H from G.

        Args:
            g (List):
        Returns:
            list:
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        parity_bits=[]
        transposed_parity_matrix=[]

        for i in range(len(self.g)):
            parity_bits.append(self.g[i][6:])           #Extraction of parity bits from generator matrix gns

        for i in range(len(parity_bits[0])):
            temp=[]
            for j in range(len(parity_bits)):
                temp.append(parity_bits[j][i])       #Transposing the Parity Matrix
            transposed_parity_matrix.append(temp)

        h_matrix =[]
        for i in range(4):
            y=transposed_parity_matrix[i]+self.g[i][:4]
            h_matrix.append(y)
        
        return h_matrix
            

    def encode(self, source_word: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        Encodes the given word and returns the new codeword as tuple.

        Args:
            source_word (tuple): m-tuple (length depends on number of data bits)
        Returns:
            tuple: n-tuple (length depends on number of total bits)
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        sourceWord = list(source_word)
        encodedWordList = []
        p5=0
        for i in range(len(self.g[0])):
            result=0
            for j in range(len(self.g)):
                result += sourceWord[j]*self.g[j][i]
            encodedWordList.append(result%2)
            p5+=(result%2)
        encodedWordList.append(p5%2)
        encodedWord = tuple(encodedWordList)
        
        return encodedWord

    def decode(self, encoded_word: Tuple[int, ...]) -> Tuple[Union[None, Tuple[int, ...]], HCResult]:
        """
        Checks the channel alphabet word for errors and attempts to decode it.
        Args:
            encoded_word (tuple): n-tuple (length depends on number of total bits)
        Returns:
            Union: (m-tuple, HCResult) or (None, HCResult)(length depends on number of data bits)
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        overallParity = 0
        
        for i in range(len(encoded_word)):
            overallParity += encoded_word[i]
            
        
        decodingWord = list(encoded_word[:-1])

        syndrome_matrix=[]

        for i in range(len(self.h)):
            result=0
            for j in range(len(self.h[-1])):
                result += decodingWord[j]*self.h[i][j]
            syndrome_matrix.append(result%2)
        
        flag=0
        pos=-1
        for i in range(len(self.h[-1])):
            h=[]
            for j in range(len(self.h)):
                h.append(self.h[j][i])
                
            
            if(h==syndrome_matrix):
                flag=1
                break
            pos+=1

        codeWord=list(encoded_word)

        if((flag==1 and overallParity%2 ==1) or (syndrome_matrix==[0,0,0,0] and overallParity%2 ==1)):
            codeWord[pos+1]=abs((codeWord[pos+1]+1)%2)
            return tuple(codeWord[:6]),HCResult.CORRECTED
                
        elif(syndrome_matrix==[0,0,0,0] and overallParity%2==0):
            return tuple(codeWord[:6]),HCResult.VALID
            
        else:
            return None,HCResult.UNCORRECTABLE
