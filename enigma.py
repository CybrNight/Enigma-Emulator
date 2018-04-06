#Written by Nathan Estrada A.K.A CyberNight A.K.A psychic2ombie
#Free to use

import numpy as np
import re
import string

w, h = 3, 3
matrix = np.matrix([[1,-2,-1],
                    [-1,1,3],
                    [1,-1,4]])

class Enigma():

    def __init__(self):
        self.matrixString = input("Input Key In Format:[[1,1,1],[1,1,1],[1,1,1]] ")
        if self.matrixString == "": self.matrixString = "[[1,-2,-1],[-1,1,3],[1,-1,4]]"
        self.matrix = np.matrix(eval(self.matrixString))
        choice = input("1:Encode 2:Decode ")

        if (choice == "1"):
            self.phrase = input("Enter phrase to encode ")

            if (self.phrase.__len__()%self.matrix.__len__() != 0):
                while (self.phrase.__len__()%self.matrix.__len__() != 0):
                    self.phrase+=" "

            self.encoded = [0 for x in range(self.phrase.__len__())]

            self.encode_string(self.phrase)
        if (choice == "2"):
            self.matricesString = input("Input list of matrices in format: [1,1,1]:[1,1,1] ")
            self.matrices = self.matricesString.split(":")
            numberString = ""
            for matrix in self.matrices:
                mx = np.matrix(matrix)
                numberString += np.array2string(np.round(np.abs(mx*self.matrix.I))).replace(".","")
            numberString = re.findall(r'\b\d+\b',numberString)
            textString = ""
            for number in numberString:
                if (number == "0"):
                    textString += " "
                else:
                    textString += string.ascii_lowercase[int(number)-1]
            print(textString)

    def encode_string(self,phrase):
        i = 0
        for l in self.phrase:
            self.encoded[i] = self.convert_char(l)
            i += 1
        arrays = self.split_list(self.encoded,int(self.encoded.__len__()/self.matrix.__len__()))
        print("Numbers:"+str(arrays))
        encoded = ""
        for a in arrays:
            mx = np.matrix(a)
            my = np.array(mx*self.matrix)
            encoded += np.array2string(my,separator=",")+":"
        print("Encoded Numbers:"+str(encoded[:-1]))
        print("Key:"+np.array2string(self.matrix,separator=","))


    def split_list(self,alist, wanted_parts=1):
        length = len(alist)
        return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]

    def convert_char(self,old):
        if len(old) != 1:
             return 0
        new = ord(old)
        if 65 <= new <= 90:
            # Upper case letter
            return new - 64
        elif 97 <= new <= 122:
            # Lower case letter
            return new - 96
        # Unrecognized character
        return 0

main = Enigma()